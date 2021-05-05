from flask import Flask


web_app = Flask(__name__)


@web_app.route('/')
def hello_world():
    return 'Hello, World!'


@web_app.route('/login')
def user_login():
    return 'Login'


@web_app.route('/signup')
def user_signup():
    return 'Signup'


@web_app.route('/user/')
def user_home():
    return 'User'
