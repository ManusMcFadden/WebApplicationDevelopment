from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from .models import User

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(email):
    return User.query.get(email)

migrate = Migrate(app, db)

from app import views, models

logging.basicConfig(level=logging.DEBUG)