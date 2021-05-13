import datetime
import logging
import re

import bcrypt
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
    _email = Column(String(length=150, ), unique=True)
    _username = Column(String(length=60), nullable=False)
    _password = Column(String(length=128))
    _start_weight = Column(Float(precision=2), nullable=False)
    goal_weight = Column(Float(precision=2), nullable=True)

    weight_entries = relationship('WeightEntry', back_populates='user',
                                  cascade='all, delete',
                                  passive_deletes=True
                                  )
    set_entries = relationship('SetEntry', back_populates='user',
                               cascade='all, delete',
                               passive_deletes=True
                               )

    def __init__(self, username, email, password, start_weight, goal_weight, date=DATETODAY):
        self.username = username
        self.email = email
        self.password = password
        self.date = date
        self.start_weight = start_weight
        self.goal_weight = goal_weight

    def __str__(self):
        return f'Name: {self._username} - Email: {self._email} Password: {self._password}' \
               f'- Start Weight: {self._start_weight} - Goal Weight: {self.goal_weight}'

    def __repr__(self):
        return f'{__class__.__name__}({self._username}, {self._email}, ' \
               f'{self._password}, {self._start_weight}, {self.goal_weight})'

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        value = self.validate_username(username)
        if username == value:
            self._username = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        value = self.validate_email(email)
        if email == value:
            self._email = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        value = self.validate_password(password)
        if password == value:
            value = value.encode(encoding='utf-8')
            hashed_pw = self.hash_password(value)
            self._password = hashed_pw

    @property
    def start_weight(self):
        return self._start_weight

    @start_weight.setter
    def start_weight(self, weight):
        weight = WeightEntry(weight, self.date)
        self._start_weight = getattr(weight, 'weight')

    def check_password_hash(self, password):
        password = password.encode(encoding='utf-8')
        if bcrypt.checkpw(password, self._password):
            return None
        else:
            return 'Incorrect password.'

    @staticmethod
    def hash_password(password):
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashed_pw

    @staticmethod
    def validate_username(username):
        """Validates whether or not given username conforms to correct username parameters and either returns the
        username or a list of errors."""
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
        elif len(username) > 60:
            error = f'Usernames must not exceed 60 characters in length.'
            errors.append(error)
        if re.match('^[^a-zA-Z0-9]', username):
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
        """Validates whether or not given email conforms to email pattern standards and either returns the email or
        a list of errors."""
        errors = []
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
        if len(errors) > 0:
            return errors

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
        elif len(password) > 128:
            error = 'Passwords cannot exceed 128 characters in length.'
            errors.append(error)
        if len(errors) > 0:
            return errors
        else:
            return password


class WeightEntry(db_class):
    """Define"""

    __tablename__ = 'weight_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    _date = Column(Date, index=True, nullable=False)
    weight = Column(Float(precision=2), nullable=False)

    user = relationship("User", back_populates='weight_entries')

    def __init__(self, weight, date=DATETODAY):
        self.weight = weight
        self.date = date

    def __str__(self):
        return f'Weight: {self.weight} | Date: {self.date}'

    def __repr__(self):
        return f'{__class__.__name__}({self.weight}, {self.date}'

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        date_entry = DateEntry(date)
        self._date = getattr(date_entry, 'date')

    @staticmethod
    def value_validation(value):
        """Validates value parameter as being an instance of either int or float and tries to convert to float
        if it is not. If a value error occurs, it logs the exception and returns. Returns the value otherwise"""
        if not (isinstance(value, (int, float))):
            try:
                value = float(value)
            except ValueError:
                logger.exception('Value error encountered.')
                return
        return value

    @staticmethod
    def sort(obj_list, key=lambda x: x[0], reverse=False):
        """Sorts the list of objects by key, which defaults to date, in ascending order."""
        sorted_list = sorted(obj_list, key=key, reverse=reverse)
        return sorted_list

    @staticmethod
    def calculate_net_change(start_val, end_val):
        """Subtracts end value from start value to determine net change and returns absolute float."""
        net_change = abs(getattr(start_val, 'weight') - getattr(end_val, 'weight'))
        return net_change

    @staticmethod
    def calculate_delta(start_val, end_val, start_date, end_date):
        """Calculates delta based on difference between starting value and end value and length of time between the
        starting date and end date. Returns a float."""
        time_delta = getattr(end_date, '_date') - getattr(start_date, '_date')
        weight = getattr(start_val, 'weight') - getattr(end_val, 'weight')
        if weight < 0:
            delta = -(weight / time_delta.days)
        else:
            delta = weight / time_delta.days
        return delta

    @staticmethod
    def calculate_time_to_goal(start_val, goal_val, delta):
        """Calculates days until the goal value is reached and returns a tuple of days left and the date upon
        which the goal will be achieved."""
        days = abs((getattr(start_val, 'weight') - goal_val) / delta)
        end_date = DATETODAY + datetime.timedelta(days=days)
        return days, end_date


class SetEntry(WeightEntry):
    """Define"""

    __tablename__ = 'lifting_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    _date = Column(Date, index=True, nullable=False)
    lift = Column(String(length=30), nullable=False)
    weight = Column(Float(precision=2), nullable=False)
    reps = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)
    rpe = Column(Float(precision=1), nullable=True)

    user = relationship("User", back_populates='set_entries')

    __mapper_args__ = {
        'concrete': True
    }

    def __init__(self, lift, weight, reps, rpe=None, date=DATETODAY):
        super().__init__(weight, date)
        self.lift = lift
        self.weight = weight
        self.reps = reps
        self.volume = self.calculate_volume()
        self.rpe = rpe
        self.date = date

    def __str__(self):
        return f'Lift: {self.lift} | Weight: {self.weight} | Reps: {self.reps} | RPE: {self.rpe} | Date: {self.date}'

    def __repr__(self):
        return f'{__class__.__name__}({self.lift} {self.weight}, {self.reps}, {self.rpe}, {self.date})'

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        date_entry = DateEntry(date)
        self._date = getattr(date_entry, 'date')

    def calculate_percentage_of_1_rep_max(self):
        """Calculates one-rep max using Brzycki formula and returns tuple of one-rep max and percentage of
        one-rep max based on the set.
        """
        one_rep_max = self.weight / (1.0278 - 0.0278 * self.reps)
        percentage = (self.weight / one_rep_max) * 100
        return percentage, one_rep_max

    def calculate_volume(self):
        """Multiplies weight and reps to determine volume and returns an integer."""
        volume = self.weight * self.reps
        return volume

    @staticmethod
    def average_rpe(sets):
        """Averages RPE for tuple of set objects and returns a float."""
        average = (sum(getattr(set, 'rpe', 0) for set in sets)) / len(
            [set for set in sets if getattr(set, 'rpe') is not None])
        return average

    @staticmethod
    def calculate_total_reps(sets):
        """Sums reps for tuple of set objects and returns an integer."""
        total_reps = sum(getattr(set, 'reps', 0) for set in sets)
        return total_reps

    @staticmethod
    def calculate_total_volume(sets):
        """Sums volume for tuple of set objects and returns an integer."""
        total_volume = sum(getattr(set, 'volume', 0) for set in sets)
        return total_volume


class DateEntry:
    """Define"""

    def __init__(self, date=DATETODAY):
        self.date = date

    def __str__(self):
        return f'{self._date.year}-{self._date.month}-{self._date.day}'

    def __repr__(self):
        return f'{__class__.__name__}({self.date})'

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        date = self.validate(date)
        self._date = self.validate(date)

    @staticmethod
    def validate(date):
        if not (isinstance(date, datetime.date)):
            try:
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                logger.exception('Value error encountered.')
                date = DATETODAY
        return date
