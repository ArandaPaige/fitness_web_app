from flask import Flask
from dotenv import load_dotenv
from os import getenv
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
DBASE = declarative_base()

load_dotenv()
SECRET_KEY = getenv('KEY')

app.config.update(
    {
        'DEBUG': True,
        'SECRET_KEY': SECRET_KEY
    }
)

from fitness_web_app import routes
from fitness_web_app import auth