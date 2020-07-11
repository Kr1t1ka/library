from flask import request, abort
from flask_restx import Namespace, Resource, fields
from sqlalchemy import or_, and_
from api_v1.main import db
from api_v1.main.endpoints.inheritances.db import Inheritances
from api_v1.main.utils import split_dict_args

api = Namespace('inheritances', description='Inheritances API')

connection_model = api.model('Inheritance',
                             model={'id_inher': fields.Integer(description='The id inher', readonly=True),
                                    'menu_id_ancestor': fields.Integer(description='The id menu1'),
                                    'menu_id_descendant': fields.Integer(description='The id menu2'),
                                    'reversible': fields.Boolean(description='reversible / not reversible'),
                                    'added': fields.DateTime(description='The date menu', readonly=True),
                                    'active': fields.Boolean(description='activated / deactivated'),
                                    'author': fields.Integer(description='author of the text')})

get_inheritances_parser = api.parser()
get_inheritances_parser.add_argument('menu_id', required=False, location='args')


@api.route('/')
class InheritancesAPI(Resource):

    @api.marshal_with(connection_model)
    @api.expect(get_inheritances_parser, validate=True)
    def get(self):
        args = split_dict_args(request.args)
        inhers = Inheritances.query
        if 'menu_id' in args:
            inhers = Inheritances.query.filter(
                or_(
                    Inheritances.menu_id_ancestor.in_(args['menu_id']),
                    and_(
                        Inheritances.menu_id_descendant.in_(args['menu_id']),
                        Inheritances.reversible == True
                    )
                )
            )
        inhers = inhers.filter_by(active=True).all()
        return inhers, 200

    @api.marshal_with(connection_model)
    @api.expect(connection_model, validate=True)
    def post(self):
        args = Inheritances(**api.payload)
        try:
            db.session.add(args)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(422, 'Something WRONG - {}'.format(e))
        return args, 201


@api.route('/<int:inheritances_id>')
class InheritanceAPI(Resource):

    @api.expect(connection_model, validate=True)
    @api.marshal_with(connection_model)
    def put(self, inheritances_id):
        connection = Inheritances.query.filter_by(id=inheritances_id)
        if not connection.first():
            return {}, 404
        connection.update(api.payload)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(422, "Something WRONG - {}".format(e))
        return connection.first(), 200

    @api.expect(connection_model, validate=True)
    @api.marshal_with(connection_model)
    def delete(self, inheritances_id):
        connection = Inheritances.query.filter_by(id=inheritances_id)
        if not connection.first():
            return {}, 404
        connection.update({'active': False})
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(422, "Something WRONG - {}".format(e))
        return connection.first(), 200
