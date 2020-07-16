from flask import request, abort
from flask_restx import Namespace, Resource, fields

from api_v1.main import db
from api_v1.main.endpoints.menu.db import Menu
from api_v1.main.utils import split_dict_args
from api_v1.main.endpoints.menu.api import menu_model
from api_v1.main.endpoints.replace_utils import text_replace


api = Namespace('search', description='search API')

search_parser = api.parser()
search_parser.add_argument('text', required=False, location='args')


@api.route('/')
class SearchAPI(Resource):

    @api.marshal_with(menu_model)
    @api.expect(search_parser)
    def get(self):
        args = split_dict_args(request.args, ['text'])

        if 'text' in args:
            res = Menu.query.filter(Menu.name.in_(args['text']))
            menu = res.filter_by(active=True).all()
            text_replace(menu)
            return menu, 200
        else:
            return {}, 404
