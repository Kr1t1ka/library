from flask import request
from flask_restx import Namespace, Resource, fields

from api_v1.main import db
from api_v1.main.endpoints.menu.menu import Menu, Inheritances
from api_v1.main.utils import split_dict_args

api = Namespace("library_api", description="Library API")


menu_model = api.model('Menu', model={'id': fields.Integer(description='The id menu', readonly=True),
                                      'Name': fields.String,
                                      'Text': fields.String})


menu_parser = api.parser()
menu_parser.add_argument("menu_id", required=False, location="args")


@api.route("/")
class MenuID(Resource):
    @api.marshal_with(menu_model)
    @api.expect(menu_parser)
    def get(self):
        args = split_dict_args(request.args)

        if "menu_id" in args:
            menu_select = Menu.query.filter(Menu.id.in_(args["menu_id"]))

        menu = menu_select.all()
        return menu, 200

    @api.expect(menu_model)
    def post(self):
        menu = api.payload

        name = menu['Name']
        text = menu['Text']

        article = Menu(name=name, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return "Done"
        except:
            return "Error_DB"

