from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from os import getenv
from pathlib import Path

BASE_DIR = Path().resolve()
DATABASE = 'test.db'
DATABASE_PATH = BASE_DIR / DATABASE

app = Flask(__name__.split('.')[0])

load_dotenv()
SECRET_KEY = getenv('KEY')

app.config.update(
    {
        'DEBUG': True,
        'SECRET_KEY': SECRET_KEY,
        'SQLALCHEMY_DATABASE_URI': "sqlite:///test.db"
    }
)
DBASE = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = 'You must log in before you can enter this area.'
login_manager.login_view = 'login'

if DATABASE_PATH.exists() is False:
    from fitness_web_app.model import User
    DBASE.create_all()

from fitness_web_app import home
from fitness_web_app import auth
from fitness_web_app import userprofile
