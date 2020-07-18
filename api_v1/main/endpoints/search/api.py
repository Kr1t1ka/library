from flask import request, abort
from flask_restx import Namespace, Resource, fields
import re

from api_v1.main import db
from api_v1.main.endpoints.menu.db import Menu
from api_v1.main.utils import split_dict_args
from api_v1.main.endpoints.menu.api import menu_model
from api_v1.main.endpoints.replace_utils import text_replace
from api_v1.main.endpoints.search_utils import smart_search


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
            user_request = args['text'][0].replace('ваня', '')
            user_request = re.sub("^\s+|\n|\r|\s+$", '', user_request).split(' ')
            res = smart_search(user_request)

            return res, 200
        else:
            return {}, 404
