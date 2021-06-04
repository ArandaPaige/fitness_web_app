from flask import render_template, flash, redirect, url_for
from fitness_web_app import app, DBASE
from fitness_web_app.model import User, WeightEntryForm, WeightEntry, SetEntryForm, SetEntry
from flask_login import login_required, current_user


@app.route("/profile/", methods=['GET'])
@login_required
def profile():
    form = WeightEntryForm()
    if form.validate_on_submit():
        weight_entry = WeightEntry(current_user.id, form.weight.data, form.date.data)
        DBASE.add(weight_entry)
        DBASE.commit()
    return render_template('profile.html', title='Profile', form=form)


@app.route("/profile/weight_history", methods=['GET'])
@login_required
def weight_history():
    form = WeightEntryForm()
    if form.validate_on_submit():
        weight_entry = WeightEntry(current_user.id, form.weight.data, form.date.data)
        DBASE.add(weight_entry)
        DBASE.commit()
    return render_template('profile.html', title='Profile')


@app.route("/profile/lifting_history", methods=['GET'])
@login_required
def lifting_history():
    form = SetEntryForm()
    if form.validate_on_submit():
        set_entry = SetEntry(
            current_user.id, form.lift.data, form.weight.data, form.reps.data, form.date.data, form.rpe.data
        )
        DBASE.add(set_entry)
        DBASE.commit()
    return render_template('profile.html', title='Profile')