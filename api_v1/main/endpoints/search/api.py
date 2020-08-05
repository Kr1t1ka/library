from flask import request
from flask_restx import Namespace, Resource, fields
import re

from api_v1.main.endpoints.menu.api import menu_model
from api_v1.main.endpoints.search.utils.request_utils import *
from api_v1.main.endpoints.search.utils.response_utils import *
from api_v1.main.endpoints.replace.utils.replace_utils import text_replace

api = Namespace('search', description='search API')

search_parser = api.parser()
search_parser.add_argument('text', required=False, location='args')

search_menu_model = api.model('Menu', model={'menu': fields.Nested(api.model('menu_model', menu_model)),
                                             'rating': fields.String(description='rating of the menu')})


@api.route('/')
class SearchAPI(Resource):

    @api.marshal_with(search_menu_model)
    @api.expect(search_parser)
    def get(self):
        args = dict_args(request.args)

        if 'text' in args:
            user_request = re.sub("[\".,«»()–:!?@\-]", ' ', args['text'][0].lower())
            user_request = user_request.lstrip().rstrip().strip()
            user_request = re.sub(r'\s+', ' ', user_request)
            user_request = replace_abbr(user_request).split(' ')
            res = [processing_user_request(word) for word in user_request]
            if 'ваня' in res:
                res.remove('ваня')
            res = smart_search(res)
            return res, 200
        else:
            return {}, 404
