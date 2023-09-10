from utilities.data_utilities import DataUtilities

from controllers.helpers.login_helpers import login_required, getLoggedInUser
from controllers.helpers.controller_constants import FileNames

from models.user import User
from models.report import Report
from models.report_data import ReportData
from models.experiment import Experiment

from flask import Response, Blueprint, jsonify, request, send_file
import json, zipfile, io

reports_api = Blueprint("models-reports", __name__, url_prefix="/info/reports")

@reports_api.route("/", methods=("GET",))
@login_required
def reports():
    """
    Gets all reports
    """
    user: User = getLoggedInUser()

    if user == None:
        return Response("Unauthorized", 403)

    reports: list[dict] = []

    for report in Report.getAll():
        if report.user == user.username:
            reports.append(report.toDict())

    return jsonify(reports)

@reports_api.route("/<experiment_id>", methods=("GET", "DELETE"))
@login_required
def report(experiment_id: str):
    """
    Gets or deletes a specific report
    """
    user: User = getLoggedInUser()

    if user == None:
        return Response("Unauthorized", 403)

    report: Report = Report.get(f"{user.username}-{experiment_id}")

    if report is None:
        return Response("Report not found.", status=404)

    if request.method == "GET":
        return jsonify(report.toDict())
    elif request.method == "DELETE":
        if not report.remove():
            return Response("Could not delete report", status=500)

        experiment: Experiment = Experiment.get(f"{user.username}-{experiment_id}")
        if (experiment != None) and not experiment.remove():
            return Response("Could not delete experiment", status=500)

        return Response(status=200)

    return Response("Unknown method", status=400)

@reports_api.route("/<experiment_id>/data", methods=("GET",))
@login_required
def report_data(experiment_id: str):
    """
    Gets a specific report's data
    """
    user: User = getLoggedInUser()

    if user == None:
        return Response("Unauthorized", 403)

    report_data: ReportData = ReportData.get(f"{user.username}-{experiment_id}")

    if report_data is None:
        return Response("Report not found.", status=404)

    return jsonify(report_data.toDict())


@reports_api.route("/<experiment_id>/download", methods=("GET",))
@login_required
def report_download(experiment_id: str):
    """
    Download Zipped Report Data
    """
    user: User = getLoggedInUser()

    if user == None:
        return Response("Unauthorized", 403)

    report: Report = Report.get(f"{user.username}-{experiment_id}")
    report_data: ReportData = ReportData.get(f"{user.username}-{experiment_id}")
    experiment: Experiment = Experiment.get(f"{user.username}-{experiment_id}")

    if (report is None) or (experiment is None) or (report_data is None):
        return Response("Report not found.", status=404)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode='w') as zip_file:
        zip_file.writestr(FileNames.report.value, json.dumps(report.toDict(), indent=2).encode("utf-8"))
        zip_file.writestr(FileNames.experiment.value, json.dumps(experiment.toDict(), indent=2).encode("utf-8"))
        zip_file.writestr(FileNames.report_data.value, json.dumps(report_data.toDict(), indent=2).encode("utf-8"))

        if report.datapoints > 0:
            if report_data.data[0][1]["base"] != {}:
                base_data: list[dict] = []

                for info in report_data.data:
                    base_data.append({"timestamp": info[0]})
                    base_data[-1].update(info[1]["base"])

                zip_file.writestr(FileNames.base_data_csv.value, DataUtilities.DictToCSV(base_data).encode("utf-8"))

            if report_data.data[0][1]["carriage"] != {}:
                carriage_data: list[dict] = []

                for info in report_data.data:
                    for c_info in info[1]["carriage"]:
                        carriage_data.append({"timestamp": info[0]})
                        carriage_data[-1].update(c_info)

                zip_file.writestr(FileNames.carriage_data_csv.value, DataUtilities.DictToCSV(carriage_data).encode("utf-8"))

    zip_buffer.seek(0)
    return send_file(zip_buffer, download_name=f"{experiment_id}.zip", mimetype="application/zip", as_attachment=True)


@reports_api.route("/upload", methods=("POST",))
@login_required
def report_upload():
    """
    Upload Zipped Report Data
    """
    user: User = getLoggedInUser()
    if user == None:
        return Response("Unauthorized", 403)

    for file in request.files.values():
        report_info: bytes = None
        experiment_info: bytes = None
        report_data_info: bytes = None

        with zipfile.ZipFile(io.BytesIO(file.stream.read()), mode='r') as zip_file:
            for zip_info in zip_file.infolist():
                if zip_info.filename == FileNames.report.value:
                    report_info = zip_file.read(zip_info)
                elif zip_info.filename == FileNames.experiment.value:
                    experiment_info = zip_file.read(zip_info)
                elif zip_info.filename == FileNames.report_data.value:
                    report_data_info = zip_file.read(zip_info)

        if report_info is None:
            return Response(f"{FileNames.report.value} not found.", status=404)
        if experiment_info is None:
            return Response(f"{FileNames.experiment.value} not found.", status=404)
        if report_data_info is None:
            return Response(f"{FileNames.report_data.value} not found.", status=404)

        report: Report = Report.fromDict(json.loads(report_info))
        report.user = user.username
        if report.exists():
            return Response(f"{report.experiment} already exists. Cannot import it.", 409)

        experiment: Experiment = Experiment.fromDict(json.loads(experiment_info))
        experiment.user = user.username
        if experiment.exists():
            return Response(f"{experiment.name} already exists. Cannot import it.", 409)

        report_data: ReportData = ReportData.fromDict(json.loads(report_data_info))
        report_data.user = user.username
        if report_data.exists():
            return Response(f"{report_data.experiment} already exists. Cannot import it.", 409)

        report.create()
        experiment.create()
        report_data.create()
        
    return Response("Success", status=200)