from controllers.helpers.login_helpers import maintainer_required, login_required
from utilities.environment import ENV
from utilities.security import Certificate

import os
from datetime import datetime
from flask import Blueprint, Response, jsonify, request

network_api = Blueprint("network", __name__, url_prefix="/network")


@network_api.route("/info", methods=("GET",))
@login_required
def network_info():
    return jsonify({
        "server_address": ENV.server_address,
        "server_port": ENV.server_port,
        "server_cert_dir_path": ENV.server_cert_dir_path,
    })

@network_api.route("/install-certificate", methods=("PUT",))
@maintainer_required
def network_InstallCert():
    if "file" not in request.files:
        return Response("No file has been given.", status=400)

    file = request.files['file']
    if file.filename == '':
        return Response("No file has been selected.", status=400)

    file_path: str = os.path.join(ENV.downloads_dir_path, str(datetime.now()))
    file.save(file_path)

    try:
        if Certificate.isValid(file_path):
            os.rename(file_path, os.path.join(ENV.downloads_dir_path, "cert.pfx"))
            return Response(status=200)
    except Exception as e:
        pass

    return Response("Couldn't install certificate", status=500)


@network_api.route("/generate-certificate", methods=("POST",))
@maintainer_required
def network_GenerateCert():
    try:
        if Certificate.generate(os.path.join(ENV.downloads_dir_path, "cert.pfx")):
            return Response(status=200)
    except Exception as e:
        pass

    return Response("Couldn't generate certificate", status=500)
