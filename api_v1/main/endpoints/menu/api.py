from flask import request, abort
from flask_restx import Namespace, Resource, fields

from api_v1.main import db
from api_v1.main.endpoints.menu.db import Menu
from api_v1.main.utils import split_dict_args
from api_v1.main.endpoints.replace_utils import text_replace

api = Namespace('menu', description='menu API')

menu_model = api.model('Menu', model={'id': fields.Integer(description='The id menu', readonly=True),
                                      'name': fields.String(description='The name mssssenu'),
                                      'text': fields.String(description='The text menu'),
                                      'added': fields.DateTime(description='The date menu', readonly=True),
                                      'active': fields.Boolean(description='activated / deactivated'),
                                      'author_id': fields.Integer(description='author of the text')})

menu_parser = api.parser()
menu_parser.add_argument('menu_ids', required=False, location='args')
menu_parser.add_argument('menu_names', required=False, location='args')
menu_parser.add_argument('menu_authors', type=int, required=False, location='args')
menu_parser.add_argument('text_field', type=bool, default=False, location='args')


@api.route('/')
class MenusAPI(Resource):

    @api.marshal_with(menu_model)
    @api.expect(menu_parser)
    def get(self):
        args = split_dict_args(request.args, ['menu_ids', 'menu_names', 'menu_authors'])
        menu_select = Menu.query
        if 'menu_ids' in args:
            menu_select = Menu.query.filter(Menu.id.in_(args['menu_ids']))
        if 'menu_names' in args:
            menu_select = Menu.query.filter(Menu.name.in_(args['menu_names']))
        if 'menu_authors' in args:
            menu_select = Menu.query.filter(Menu.author_id.in_(args['menu_authors']))

        menu = menu_select.filter_by(active=True).all()

        if 'text_field' in args:
            if args['text_fields']:
                text_replace(menu)

        return menu, 200

    @api.marshal_with(menu_model)
    @api.expect(menu_model, validate=True)
    def post(self):
        args = Menu(**api.payload)
        try:
            db.session.add(args)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(422, 'Something WRONG - {}'.format(e))
        return args, 201


@api.route('/<int:menu_id>')
class MenuAPI(Resource):

    @api.expect(menu_model, validate=True)
    @api.marshal_with(menu_model)
    def put(self, menu_id):
        menu = Menu.query.filter_by(id=menu_id)
        if not menu.first():
            return {}, 404
        menu.update(api.payload)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(422, "Something WRONG - {}".format(e))
        return menu.first(), 200

    @api.expect(menu_model, validate=True)
    @api.marshal_with(menu_model)
    def delete(self, menu_id):
        menu = Menu.query.filter_by(id=menu_id)
        if not menu.first():
            return {}, 404
        menu.update({'active': False})
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(422, "Something WRONG - {}".format(e))
        return menu.first(), 200
