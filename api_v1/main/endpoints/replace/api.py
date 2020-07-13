from flask import request, abort
from flask_restx import Namespace, Resource, fields

from api_v1.main import db
from api_v1.main.endpoints.replace.db import Replace
from api_v1.main.utils import split_dict_args

api = Namespace('replace', description='replace API')

replace_model = api.model('Replace', model={'id': fields.Integer(description='The id replace', readonly=True),
                                            'name': fields.String(description='The name of replacement'),
                                            'value': fields.String(description='The text replacement'),
                                            'date': fields.DateTime(description='The date added replacement',
                                                                    readonly=True),
                                            'active': fields.Boolean(description='activated / deactivated'),
                                            'author': fields.Integer(description='author of the replacement')})

replace_parser = api.parser()
replace_parser.add_argument('replace_ids', required=False, location='args')
replace_parser.add_argument('replace_names', required=False, location='args')


@api.route('/')
class ReplaceAPI(Resource):

    @api.marshal_with(replace_model)
    @api.expect(replace_parser)
    def get(self):
        args = split_dict_args(request.args)
        replace_select = Replace.query
        if 'replace_ids' in args:
            replace_select = Replace.query.filter(Replace.id.in_(args['replace_ids']))
        if 'replace_names' in args:
            replace_select = Replace.query.filter(Replace.name.in_(args['replace_names']))

        res = replace_select.filter_by(active=True).all()
        return res, 200

    @api.marshal_with(replace_model)
    @api.expect(replace_model, validate=True)
    def post(self):
        args = Replace(**api.payload)
        try:
            db.session.add(args)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(422, 'Something WRONG - {}'.format(e))
        return args, 201


@api.route('/<int:replace_id>')
class MenuAPI(Resource):

    @api.expect(replace_model, validate=True)
    @api.marshal_with(replace_model)
    def put(self, replace_id):
        res = Replace.query.filter_by(id=replace_id)
        if not res.first():
            return {}, 404
        res.update(api.payload)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(422, "Something WRONG - {}".format(e))
        return res.first(), 200

    @api.expect(replace_model, validate=True)
    @api.marshal_with(replace_model)
    def delete(self, replace_id):
        res = Replace.query.filter_by(id=replace_id)
        if not res.first():
            return {}, 404
        res.update({'active': False})
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(422, "Something WRONG - {}".format(e))
        return res.first(), 200
