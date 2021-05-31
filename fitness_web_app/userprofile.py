from flask import render_template, flash, redirect, url_for
from fitness_web_app import app, DBASE
from fitness_web_app.model import User
from flask_login import login_required, current_user


@app.route("/profile/", methods=['GET'])
def profile():
    return render_template('profile.html', title='Profile')
