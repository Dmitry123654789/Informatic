from flask import Flask
from flask_login import LoginManager

from data.db_session import global_init

app = Flask(__name__)


app.config['SECRET_KEY'] = 'super secret key'

login_manager = LoginManager()
login_manager.init_app(app)
global_init('db/informatic_questions.db')

from tools import routes
