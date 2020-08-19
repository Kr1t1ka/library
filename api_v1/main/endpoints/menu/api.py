from flask import request, abort
from flask_restx import Namespace, Resource, fields

from api_v1.main import db
from api_v1.main.endpoints.menu.db import Menu, Attachment
from api_v1.main.endpoints.inheritances.api import connection_model
from api_v1.main.utils import split_dict_args
from api_v1.main.endpoints.replace.utils.replace_utils import text_replace

api = Namespace('menu', description='menu API')

attachment_model = api.model('Attachment',
                             model={'id': fields.Integer(description='The id attachment', readonly=True),
                                    'menu_id': fields.Integer(description='Thr menu id of attachment'),
                                    'active': fields.Boolean(description='vk activated / deactivated'),
                                    'vk_active': fields.Boolean(description='vk activated / deactivated'),
                                    'telegram_active': fields.Boolean(description='telegram activated / deactivated'),
                                    'vk_attachment': fields.String(description='vk attachment'),
                                    'telegram_attachment': fields.String(description='telegram attachment')})

menu_model = api.model('Menu', model={'id': fields.Integer(description='The id menu', readonly=True),
                                      'name': fields.String(description='The name menu'),
                                      'text': fields.String(description='The text menu'),
                                      'added': fields.DateTime(description='The date menu', readonly=True),
                                      'active': fields.Boolean(description='activated / deactivated'),
                                      'author_id': fields.Integer(description='author of the text'),
                                      'tags': fields.String(description='The text menu'),
                                      'inheritances': fields.List(
                                          fields.Nested(api.model('connection_model', connection_model))),
                                      'attachment': fields.List(
                                          fields.Nested(api.model('connection_model', attachment_model)))
                                      })

menu_parser = api.parser()
menu_parser.add_argument('menu_ids', required=False, location='args')
menu_parser.add_argument('menu_names', required=False, location='args')
menu_parser.add_argument('menu_authors', type=int, required=False, location='args')
menu_parser.add_argument('filled_text', type=bool, default=False, location='args')


attachment_parser = api.parser()
attachment_parser.add_argument('menu_id', required=False, location='args')


@api.route('/')
class MenusAPI(Resource):

    @api.expect(menu_parser, validate=True)
    @api.marshal_with(menu_model)
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

        if 'filled_text' in args:
            if args['filled_text'] == 'true':
                text_replace(menu)

        if not menu:
            return {}, 404

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


@api.route('/attachment')
class AttachmentsAPI(Resource):

    @api.marshal_with(attachment_model)
    @api.expect(attachment_parser, validate=True)
    def get(self):
        args = split_dict_args(request.args)
        attachment = Attachment.query
        if 'menu_id' in args:
            attachment = Attachment.query.filter(Attachment.menu_id.in_(args['menu_id']))
        attachment = attachment.all()

        if not attachment:
            return {}, 404

        return attachment, 200

    @api.marshal_with(attachment_model)
    @api.expect(attachment_model, validate=True)
    def post(self):
        args = Attachment(**api.payload)
        try:
            db.session.add(args)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(422, 'Something WRONG - {}'.format(e))
        return args, 201


@api.route('/attachment/<int:menu_id>')
class AttachmentAPI(Resource):

    @api.expect(attachment_model, validate=True)
    @api.marshal_with(attachment_model)
    def put(self, menu_id):
        attachment = Attachment.query.filter_by(id=menu_id)
        if not attachment.first():
            return {}, 404
        attachment.update(api.payload)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(422, "Something WRONG - {}".format(e))
        return attachment.first(), 200

    @api.expect(attachment_model, validate=True)
    @api.marshal_with(attachment_model)
    def delete(self, menu_id):
        attachment = Attachment.query.filter_by(id=menu_id)
        if not attachment.first():
            return {}, 404
        attachment.update({'active': False})
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(422, "Something WRONG - {}".format(e))
        return attachment.first(), 200
