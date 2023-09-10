from controllers.models.configurations import configurations_api
from controllers.models.experiments import experiments_api
from controllers.models.modules import modules_api
from controllers.models.reports import reports_api
from controllers.models.states import states_api
from controllers.models.devices import devices_api as devices_model_api
from controllers.models.users import users_api

from controllers.services.devices import devices_api
from controllers.services.login import login_api
from controllers.services.network import network_api
from controllers.services.profile import profile_api
from controllers.services.server import server_api
from controllers.services.settings import settings_api

from flask import Blueprint

MODELS_BLUEPRINTS: tuple[Blueprint] = (
    configurations_api,
    experiments_api,
    modules_api,
    reports_api,
    states_api,
    users_api,
    devices_model_api
)

SERVICES_BLUEPRINTS: tuple[Blueprint] = (
    devices_api,
    login_api,
    network_api,
    profile_api,
    server_api,
    settings_api
)
