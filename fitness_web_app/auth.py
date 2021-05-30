from flask import render_template, flash, redirect, url_for
from fitness_web_app import app, DBASE
from fitness_web_app.model import RegistrationForm, LoginForm, User


@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(_username=form.username.data).first()
        flash(f'{form.username.data} has successfully logged in!')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.email.data, form.password.data)
        DBASE.session.add(user)
        DBASE.session.commit()
        flash(f'Account created for {form.username.data}.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)