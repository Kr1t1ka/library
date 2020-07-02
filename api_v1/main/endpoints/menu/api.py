from flask_restx import Namespace, Resource, fields
from api_v1.main.endpoints.menu.menu import Menu, Inheritances


api = Namespace("library_api", description="Library API")


@api.route("/")
class MenuID(Resource):
    def get(self):

        return 'test_123'
