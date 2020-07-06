from flask import request, abort
from flask_restx import Namespace, Resource, fields

from api_v1.main import db
from api_v1.main.endpoints.menu.menu import Inheritances
from api_v1.main.utils import split_dict_args

api = Namespace('Inheritances_api', description='Inheritances API')


connection_model = api.model('Menu', model={'id': fields.Integer(description='The id menu', readonly=True),
                                            'name': fields.String(description='The name menu')})

#TODO: запросы GET: сама связь, связь + имена связаных, все связи(активные)
# запросы POST: новая связь
# запросы PUT: изменение связи
# запросы DELETE: деактивация связи


@api.route('/')
class InheritanceAPI(Resource):

    def get(self):
        return "menu", 200
