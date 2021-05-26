from flask import render_template, request, flash, redirect, url_for
from fitness_web_app import app


@app.route("/", methods=['GET'])
def home():
    return render_template('home.html', title='Home')


@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html', title='About')


@app.route("/user", methods=['GET'])
def user():
    user_auth = True
    if not user_auth:
        redirect('login')
    return render_template('user.html', title='User')
