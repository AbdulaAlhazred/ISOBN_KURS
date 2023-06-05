from os import urandom

import flask_login
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.secret_key = urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:S123456s@localhost/ISOBN'
app.app_context().push()
db = SQLAlchemy(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам и функциям"
login_manager.login_message_category = "success"

from sweater import models, routes

db.create_all()
