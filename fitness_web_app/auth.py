from flask import render_template, flash, redirect, url_for
from fitness_web_app import app, DBASE
from fitness_web_app.model import RegistrationForm, LoginForm, User
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(_username=form.username.data).first()
        if user is None:
            flash(f'{form.username} could not be found. Please enter another username.')
        if user is not None and user.check_password_hash(form.password.data):
            login_user(user, remember=True)
            flash(f'{user.username} has successfully logged in!')
            return redirect(url_for('home'))
        else:
            flash(f'Incorrect password. Please try again.')
    return render_template('login.html', title='Login', form=form)


@app.route('/register/', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.email.data, form.password.data)
        DBASE.session.add(user)
        DBASE.session.commit()
        flash(f'Account created for {user.username}.')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/account/', methods=['POST', 'GET'])
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have been successfully logged out.')
    return redirect(url_for('home'))
