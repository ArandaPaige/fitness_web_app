from flask import render_template, flash, redirect, url_for
from fitness_web_app import app, DBASE
from fitness_web_app.model import User, WeightEntryForm, WeightEntry, SetEntryForm, SetEntry
from flask_login import login_required, current_user


@app.route("/profile/", methods=['POST', 'GET'])
@login_required
def profile():
    form = WeightEntryForm()
    if form.validate_on_submit():
        if form.date.data is None:
            weight_entry = WeightEntry(current_user.id, form.weight.data)
        else:
            weight_entry = WeightEntry(current_user.id, form.weight.data, form.date.data)
        DBASE.session.add(weight_entry)
        DBASE.session.commit()
    return render_template('profile.html', title='Profile', form=form)


@app.route("/profile/weight_history", methods=['POST', 'GET'])
@login_required
def weight_history():
    form = WeightEntryForm()
    if form.validate_on_submit():
        if form.date.data is None:
            weight_entry = WeightEntry(current_user.id, form.weight.data)
        else:
            weight_entry = WeightEntry(current_user.id, form.weight.data, form.date.data)
        DBASE.session.add(weight_entry)
        DBASE.session.commit()
    return render_template('weight_history.html', title='Profile', form=form)


@app.route("/profile/lifting_history", methods=['POST', 'GET'])
@login_required
def lifting_history():
    form = SetEntryForm()
    if form.validate_on_submit():
        if form.date.data is None:
            set_entry = SetEntry(
                current_user.id, form.lift.data, form.weight.data, form.reps.data, form.rpe.data
            )
        else:
            set_entry = SetEntry(
                current_user.id, form.lift.data, form.weight.data, form.reps.data, form.rpe.data, form.date.data
            )
        DBASE.session.add(set_entry)
        DBASE.session.commit()
    return render_template('lifting_history.html', title='Profile', form=form)
