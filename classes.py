import datetime
import logging

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

DATETODAY = datetime.date.today()

db_class = declarative_base()


class User(db_class):
    """Define"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=150), nullable=False)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'(Name: {self.name})'

    def __repr__(self):
        return f'{__class__.__name__}({self.name})'


class WeightEntry(db_class):
    """Define"""

    __tablename__ = 'weight_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    weight = Column(Float(precision=2), nullable=False)
    user = relationship(User)

    def __init__(self, date, weight):
        self.date = date
        self.weight = weight

    def __str__(self):
        return f'Date: {self.date} | Weight: {self.weight}'

    def __repr__(self):
        return f'{__class__.__name__}({self.date}, {self.weight}'

    @staticmethod
    def value_validation(value):
        """Validates value parameter as being an instance of either int or float and raises TypeError if not."""
        if not (isinstance(value, int) or isinstance(value, float)):
            logger.exception('Type error raised.')
            raise TypeError
        return

    @staticmethod
    def sort(weight_list, key=lambda x: x[0], reverse=False):
        sorted_list = sorted(weight_list, key=key, reverse=reverse)
        return sorted_list

    @staticmethod
    def calculate_delta(start_val, end_val, start_date, end_date):
        time_delta = end_date - start_date
        weight = start_val - end_val
        if weight <= 0:
            delta = weight / time_delta.days
        else:
            delta = -(weight / time_delta.days)
        return delta

    @staticmethod
    def calculate_net_change(start_val, end_val):
        net_change = abs(start_val - end_val)
        return net_change

    @staticmethod
    def calculate_time_to_goal(start_val, goal_val, delta):
        diff = start_val - goal_val
        days = abs(int(diff / delta))
        end_date = DATETODAY + datetime.timedelta(days=days)
        return days, end_date


class SetEntry(WeightEntry):
    """Define"""

    __tablename__ = 'lifting_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users'))
    date = Column(Date, nullable=False)
    lift = Column(String, nullable=False)
    weight = Column(Float(precision=2), nullable=False)
    reps = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)
    rpe = Column(Float, nullable=True)
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
        return f'(Date: {self.date} | Weight: {self.weight} | Reps: {self.reps})'

    def __repr__(self):
        return f'{__class__.__name__}({self.date}, {self.weight}, {self.reps})'

    def calculate_percentage_of_1_rep_max(self):
        one_rep_max = self.weight / (1.0278 - 0.0278 * self.reps)
        percentage = self.weight / one_rep_max
        return percentage, one_rep_max

    def calculate_volume(self):
        volume = self.weight * self.reps
        return volume

    @staticmethod
    def average_rpe(sets):
        average = (sum(obj.getattr(obj, 'rpe', 0) for obj in sets)) / len(sets)
        return average

    @staticmethod
    def calculate_total_reps(sets):
        total_reps = sum(obj.getattr(obj, 'reps', 0) for obj in sets)
        return total_reps

    @staticmethod
    def calculate_total_volume(sets):
        total_volume = sum(obj.getattr(obj, 'volume', 0) for obj in sets)
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
        pass

    def format_date(self):
        """Validates date parameter if it matches ISO format and raises ValueError if it does not."""
        date = '-'.join((self.year, self.month, self.day))
        try:
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            logger.exception('Value error raised.')
            raise ValueError
        else:
            return date_obj
