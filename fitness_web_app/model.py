from functools import reduce
import database
import classes
import datetime

DATETODAY = datetime.date.today()


def deepgetattr(obj, attr):
    """Recurses through an attribute chain to get the ultimate value."""
    return reduce(getattr, attr.split('.'), obj)


def retrieve_user(username):
    filter_args = {'_username': username}
    user = database.retrieve_object(classes.User, filter_args)
    return user


def create_user(username, email, password):
    user = classes.User(username, email, password)
    return user


def new_weight_entry(user_id, weight, date=DATETODAY):
    weight_entry = classes.WeightEntry(user_id, weight, date)
    return weight_entry


def new_lift_entry(user_id, lift, weight, reps, date=DATETODAY):
    lift_entry = classes.SetEntry(user_id, lift, weight, reps, date)
    return lift_entry


def add_instance(instance):
    database.add_object(instance)


def update_instance(obj_class, obj_ref, instance):
    pass


def del_instance(obj_class, obj_ref):
    pass
