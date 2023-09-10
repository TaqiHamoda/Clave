from controllers.helpers.login_helpers import login_required
from models.device import Device

from flask import Response, Blueprint, jsonify

devices_api = Blueprint("models-devices", __name__, url_prefix="/info/devices")

@devices_api.route("/", methods=("GET",))
@login_required
def devices():
    """
    Gets all devices.
    """
    return jsonify([device.toDict() for device in Device.getAll()])

@devices_api.route("/<module_id>", methods=("GET",))
@login_required
def device(module_id: str):
    """
    Gets a specific device
    """
    device: Device = Device.get(module_id)

    if device is None:
        return Response("Device not found.", status=404)

    return jsonify(device.toDict())
