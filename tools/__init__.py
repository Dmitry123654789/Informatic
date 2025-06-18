from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

from api.resourse_login import LoginResource
from data.db_session import global_init

app = Flask(__name__)

# api пользователей
api = Api(app)
api.add_resource(LoginResource, '/api/login')

app.config['SECRET_KEY'] = 'super secret key'

login_manager = LoginManager()
login_manager.init_app(app)
global_init('db/informatic_questions.db')

from tools import routes
