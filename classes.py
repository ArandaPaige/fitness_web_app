import datetime
import logging
import re

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

logger = logging.getLogger(__name__)

DATETODAY = datetime.date.today()

db_class = declarative_base()


class User(db_class):
    """Define"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(length=150,), index=True, unique=True)
    username = Column(String(length=60), nullable=False)
    password = Column(String(length=128))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __str__(self):
        return f'(Name: {self.name})'

    def __repr__(self):
        return f'{__class__.__name__}({self.name})'

    @staticmethod
    def validate_username(username):
        errors = []
        if not isinstance(username, str):
            try:
                username = str(username)
            except ValueError:
                logger.exception('Value error encountered')
                return f'Cannot convert {username} to username format.'
        if len(username) < 8:
            error = f'Username must contain a minimum of 8 characters.'
            errors.append(error)
        if not re.match('^[a-zA-Z0-9]?', username):
            error = f'Usernames must start with an alpha-numeric character.'
            errors.append(error)
        if not re.match('[-]?[!]?[_]?[?]?', username[1:]):
            error = f'Usernames can only contain one each of the following special characters: !, ?, _, and -'
            errors.append(error)
        if len(errors) > 0:
            return errors
        else:
            return username

    @staticmethod
    def validate_email(email):
        error = []
        if not isinstance(email, str):
            try:
                email = str(email)
            except ValueError:
                logger.exception('Value error encountered.')
                return f'Cannot convert {email} to email format.'
        prefix, domain = email.split('@', 1)
        prefix_match = re.match('^[a-zA-Z0-9]+[._-]?[a-zA-Z0-9]+', prefix)
        domain_match = re.match('^[a-zA-Z0-9]+[-]?[a-zA-Z0-9]+[.]?[a-zA-Z]', domain)
        if prefix_match and domain_match:
            email = '@'.join((prefix, domain))
            return email
        elif prefix_match is None:
            pass
        elif domain_match is None:
            pass
        if error:
            return error

    @staticmethod
    def validate_password(password):
        errors = []
        if not isinstance(password, str):
            try:
                password = str(password)
            except ValueError:
                logger.exception('Value error encountered.')
                return f'Cannot convert password to password format.'
        if len(password) < 8:
            error = 'Passwords must contain a minimum of 8 characters.'
            errors.append(error)


class WeightEntry(db_class):
    """Define"""

    __tablename__ = 'weight_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    weight = Column(Float(precision=2), nullable=False)
    user = relationship(User)

    def __init__(self, date, weight):
        self.date = DateEntry(date)
        self.weight = weight

    def __str__(self):
        return f'Date: {self.date} | Weight: {self.weight}'

    def __repr__(self):
        return f'{__class__.__name__}({self.date}, {self.weight}'

    @staticmethod
    def value_validation(value):
        """Validates value parameter as being an instance of either int or float and raises TypeError if not."""
        if not (isinstance(value, (int, float))):
            logger.exception('Type error encountered.')
        return value

    @staticmethod
    def sort(obj_list, key=lambda x: x[0], reverse=False):
        """Sorts the list of objects by key, which defaults to date, in ascending order."""
        sorted_list = sorted(obj_list, key=key, reverse=reverse)
        return sorted_list

    @staticmethod
    def calculate_net_change(start_val, end_val):
        """Subtracts end value from start value to determine net change and returns absolute float."""
        net_change = abs(start_val - end_val)
        return net_change

    @staticmethod
    def calculate_delta(start_val, end_val, start_date, end_date):
        """Calculates delta based on difference between starting value and end value and length of time between the
        starting date and end date. Returns a float."""
        time_delta = end_date - start_date
        weight = start_val - end_val
        if weight <= 0:
            delta = weight / time_delta.days
        else:
            delta = -(weight / time_delta.days)
        return delta

    @staticmethod
    def calculate_time_to_goal(start_val, goal_val, delta):
        """Calculates days until the goal value is reached and returns a tuple of days left and the date upon
        which the goal will be achieved."""
        days = abs((start_val - goal_val) / delta)
        end_date = DATETODAY + datetime.timedelta(days=days)
        return days, end_date


class SetEntry(WeightEntry):
    """Define"""

    __tablename__ = 'lifting_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    lift = Column(String(length=30), nullable=False)
    weight = Column(Float(precision=2), nullable=False)
    reps = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)
    rpe = Column(Float(precision=1), nullable=True)
    user = relationship(User)

    __mapper_args__ = {
        'concrete': True
    }

    def __init__(self, lift, date, weight, reps, rpe=None):
        super().__init__(date, weight)
        self.date = DateEntry(date)
        self.lift = lift
        self.weight = weight
        self.reps = reps
        self.volume = self.calculate_volume()
        self.rpe = rpe

    def __str__(self):
        return f'Date: {self.date} | Weight: {self.weight} | Reps: {self.reps} | RPE: {self.rpe}'

    def __repr__(self):
        return f'{__class__.__name__}({self.date}, {self.weight}, {self.reps}, {self.rpe})'

    def calculate_percentage_of_1_rep_max(self):
        """Calculates one-rep max using Brzycki formula and returns tuple of one-rep max and percentage of
        one-rep max based on the set.
        """
        one_rep_max = self.weight / (1.0278 - 0.0278 * self.reps)
        percentage = self.weight / one_rep_max
        return percentage, one_rep_max

    def calculate_volume(self):
        """Multiplies weight and reps to determine volume and returns an integer."""
        volume = self.weight * self.reps
        return volume

    @staticmethod
    def average_rpe(sets):
        """Averages RPE for tuple of set objects and returns a float."""
        average = (sum(set.getattr(set, 'rpe', 0) for set in sets)) / len(sets)
        return average

    @staticmethod
    def calculate_total_reps(sets):
        """Sums reps for tuple of set objects and returns an integer."""
        total_reps = sum(set.getattr(set, 'reps', 0) for set in sets)
        return total_reps

    @staticmethod
    def calculate_total_volume(sets):
        """Sums volume for tuple of set objects and returns an integer."""
        total_volume = sum(set.getattr(set, 'volume', 0) for set in sets)
        return total_volume


class DateEntry:
    """Define"""

    def __init__(self, date=DATETODAY):
        self.date = date
        self.year = None
        self.month = None
        self.day = None

    def __str__(self):
        return f'{self.year}-{self.month}-{self.day}'

    def __repr__(self):
        return f'{__class__.__name__}({self.date})'

    def validate(self):
        if not (isinstance(self.date, datetime.date)):
            try:
                self.date = datetime.datetime.strptime(self.date, '%Y-%m-%d')
            except ValueError:
                logger.exception('Value error encountered.')

    def format_date(self):
        """Validates date parameter if it matches ISO format and raises ValueError if it does not."""
        date = '-'.join((self.year, self.month, self.day))
        try:
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            logger.exception('Value error encountered.')
        else:
            return date_obj
