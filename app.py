from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api_v1.main import create_app, db
from api_v1 import v1_api
from flask import url_for
import os
from flask_restx import Api


env_build = os.getenv("BUILD") or 'dev'
app = create_app(env_build)
app.register_blueprint(v1_api, url_prefix='/api/v1')

app.app_context().push()

@property
def specs_url(self):
    """Monkey patch for HTTPS"""
    return url_for(self.endpoint('specs'), _external=True, _scheme='https')
if env_build in ['dev', 'prod']:
    Api.specs_url = specs_url

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return "Hello world!"


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'content-type,headers,authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == '__main__':
    manager.run()
