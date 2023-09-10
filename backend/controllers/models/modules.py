from controllers.helpers.login_helpers import login_required, maintainer_required
from controllers.helpers.controller_constants import ModuleConstant

from models.module import Module
from models.image import Image

from utilities.environment import ENV
from engines.module.module_info import ModuleInfo
from engines.module.module_handler import ModuleHandler

from flask import Response, Blueprint, jsonify, request, send_file
import zipfile, io, shutil, os

modules_api = Blueprint("models-modules", __name__, url_prefix="/info/modules")

@modules_api.route("/", methods=("GET",))
@login_required
def modules_modules():
    """
    Gets all modules
    """
    return jsonify([module.toDict() for module in Module.getAll()])

@modules_api.route("/<module_id>", methods=("GET",))
@login_required
def modules_module(module_id: str):
    """
    Gets a specific module
    """
    module: Module = Module.get(module_id)

    if module is None:
        return Response("Module not found.", status=404)

    return jsonify(module.toDict())

@modules_api.route("/<module_id>/image", methods=("GET",))
@login_required
def modules_image(module_id: str):
    """
    Gets a specific module's image
    """
    module: Module = Module.get(module_id)
    if module is None:
        return Response("Module not found.", status=404)

    image: Image = Image.get(module.image_name)

    if image is None:
        return Response("Image not found", status=404)

    return jsonify(image.toDict())


# TODO: Optimize using CouchDB filtering
@modules_api.route("/images", methods=("GET",))
@login_required
def modules_images():
    """
    Gets all modules' images
    """
    modules: list[Module] = Module.getAll()
    images: list[dict] = []

    for module in modules:
        image: Image = Image(module.name).get()
        if image is None:
            continue

        images.append(image.toDict())

    return jsonify(images)


@modules_api.route("/<module_id>/download", methods=("GET",))
@login_required
def modules_download(module_id: str):
    """
    Download a module.
    """
    module: Module = Module.get(module_id)
    if module is None:
        return Response("Module not found.", status=404)
    elif not os.path.isdir(f"{ENV.module_path}/{module.dir_name}"):
        return Response("Module not installed on system.", status=404)

    zip_buffer = io.BytesIO()
    dir_name = f"{ENV.module_path}/{module.dir_name}"
    with zipfile.ZipFile(zip_buffer, mode='w') as zip_file:
        for root, dirs, files in os.walk(dir_name):
            for file in files:
                zip_file.write(os.path.join(root, file), os.path.join(root.replace(dir_name, module.dir_name), file))

    zip_buffer.seek(0)
    return send_file(zip_buffer, download_name=f"{module.dir_name}.zip", mimetype="application/zip", as_attachment=True)


@modules_api.route("/install", methods=("POST",))
@maintainer_required
def modules_install():
    """
    Install a module zip file.
    """
    for file in request.files.values():
        with zipfile.ZipFile(io.BytesIO(file.stream.read()), mode='r') as zip_file:
            for zip_info in zip_file.infolist():
                if zip_info.is_dir():
                    module_file_exists: bool = zip_file.NameToInfo.get(f"{zip_info.filename}{ModuleConstant.module.value}") is not None
                    config_file_exists: bool = zip_file.NameToInfo.get(f"{zip_info.filename}{ModuleConstant.config.value}") is not None

                    try:
                        if module_file_exists and config_file_exists:
                            zip_file.extractall(ENV.module_path, members=[z for z in zip_file.infolist() if zip_info.filename in z.filename])

                            installed_module: Module = Module.loadFromDir(zip_info.filename)
                            if installed_module is None:
                                return Response(f"Faced issue with installing module {zip_info.filename}.", 500)

                            if not ModuleInfo.exists(installed_module.name):
                                module_info: ModuleInfo = ModuleInfo(installed_module.name)
                                module_handler: ModuleHandler = ModuleHandler(module_info)

                                module_handler.run(installed_module.dir_name)

                    except Exception as e:
                        return Response(f"Faced issue with installing module {zip_info.filename}: {e}.", 500)

    return Response("Success", status=200)


@modules_api.route("/<module_id>/uninstall", methods=("DELETE",))
@maintainer_required
def modules_uninstall(module_id: str):
    """
    Uninstall a module.
    """
    module: Module = Module.get(module_id)
    if module is None:
        return Response("Module not found.", status=404)

    if not module.remove():
        return Response("Couldn't delete interface.", status=500)

    try:
        shutil.rmtree(f"{ENV.module_path}/{module.dir_name}")
    except Exception as e:
        return Response(f"Couldn't remove interfec from system: {e}.", status=500)

    return Response(status=200)
