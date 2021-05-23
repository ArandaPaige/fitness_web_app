from flask import Flask

app = Flask(__name__)


from fitness_web_app import routes
