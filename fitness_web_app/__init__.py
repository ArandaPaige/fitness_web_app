from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

load_dotenv()
SECRET_KEY = getenv('KEY')

app.config.update(
    {
        'DEBUG': True,
        'SECRET_KEY': SECRET_KEY,
        'SQLALCHEMY_DATABASE_URI': "sqlite:///example.sqlite"
    }
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
DBASE = SQLAlchemy(app)

from fitness_web_app import routes
from fitness_web_app import auth