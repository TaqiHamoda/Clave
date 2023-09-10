from controllers.helpers.login_helpers import login_required
from utilities.environment import ENV

import platform, psutil
from flask import Blueprint, jsonify

server_api = Blueprint('server', __name__, url_prefix="/server")

# TODO: A controller to get all logs available
# TODO: Add an api to change logging level

@server_api.route("/info", methods=("GET",))
def server_info():
    # Returns Open-CR info and system info
    return jsonify({
        "version": ENV.version,
        "server": {
            "system": platform.system(),  # e.g. Windows, Linux, Darwin
            "architecture": platform.architecture(),  # e.g. 64-bit
            "machine": platform.machine(),  # e.g. x86_64
            "hostname": platform.node(),  # Hostname
        }
    })


@server_api.route("/resources", methods=("GET",))
@login_required
def server_resources():
    # Returns server resources: cpu, memory, disk
    # Info is in bytes unless said otherwise

    disk = psutil.disk_usage('/')
    memory = psutil.virtual_memory()

    return jsonify({
        "cpu_percent": psutil.cpu_percent(),
        "memory_free": memory[4],
        "memory_total": memory[0],
        "disk_free": disk[2],
        "disk_total": disk[0],
    })
