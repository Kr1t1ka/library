from flask_restx import Api
from flask import Blueprint

from api_v1.main.endpoints.inheritances.api import api as inheritances_api
from api_v1.main.endpoints.menu.api import api as menu_api
import pprint
import os

printer = pprint.PrettyPrinter().pprint
API_NAME = "1NFORM {} 2020 API".format(os.getenv("NAME") or "Local")
v1_api = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(
    v1_api,
    version='1.0',
    title=API_NAME,
    description=API_NAME,
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(menu_api)
api.add_namespace(inheritances_api)
