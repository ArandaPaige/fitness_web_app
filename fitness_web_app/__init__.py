from flask import Flask
from dotenv import load_dotenv
from os import getenv

app = Flask(__name__)

load_dotenv()
SECRET_KEY = getenv('KEY')

app.config.update(
    {
        'DEBUG': True,
        'SECRET KEY': SECRET_KEY
    }
)

from fitness_web_app import routes
