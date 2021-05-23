from fitness_web_app import app
from flask import render_template, request


@app.route('<usr>')
def user(usr):
    return render_template('user.html')

