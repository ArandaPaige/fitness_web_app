import logging
import datetime

logger = logging.getLogger(__name__)

DATETODAY = datetime.date.today()


class User:
    """Define"""

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __str__(self):
        return f'(ID: {self.user_id} | Name: {self.name})'

    def __repr__(self):
        return f'{__class__.__name__}({self.user_id}, {self.name})'


class WeightEntry:
    """Define"""

    def __init__(self, date, weight):
        self.date = date
        self.weight = weight
        self.collection = ()

    def __str__(self):
        return f'Date: {self.date} | Weight: {self.weight}'

    def __repr__(self):
        return f'{__class__.__name__}({self.date}, {self.weight}'

    @staticmethod
    def date_validation(date):
        """Validates date parameter if it matches ISO format and raises ValueError if it does not."""
        try:
            date = datetime.date.strftime(date, '%Y-%m-%d')
        except ValueError:
            logger.exception('Value error raised.')
            raise ValueError
        return date

    @staticmethod
    def value_validation(value):
        """Validates value parameter as being an instance of either int or float and raises TypeError if not."""
        if not (isinstance(value, int) or isinstance(value, float)):
            logger.exception('Type error raised.')
            raise TypeError
        else:
            return value


class SetEntry(WeightEntry):
    """Define"""

    def __init__(self, date, weight, reps):
        super().__init__(date, weight)
        self.date = date
        self.weight = weight
        self.reps = reps
        self.RPE = None
        self.volume = None
        self.collection = ()

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


class SetsEntry:
    """Define"""

    def __init__(self, date, *set_objs):
        self.date = date
        self.sets = len(set_objs)
        self.set_list = set_objs
        self.volume = None

    def __str__(self):
        return f'(Date: {self.date} | Sets: {self.sets})'

    def __repr__(self):
        return f'{__class__.__name__}({self.date}, {self.sets})'

    def average_rpe(self):
        average = int((sum(obj.getattr(obj, 'RPE', 0) for obj in self.set_list)) / self.sets)
        return average

    def calculate_total_reps(self):
        total = sum(obj.getattr(obj, 'reps', 0) for obj in self.set_list)
        return total

    def calculate_volume(self):
        self.volume = sum(obj.getattr(obj, 'volume', 0) for obj in self.set_list)


class WeightHistory:
    """Define"""

    def __init__(self, weight_list=None):
        self.list = weight_list

    def __str__(self):
        return f'(Weight History: {self.list})'

    def __repr__(self):
        return f'{__class__.__name__}({self.list})'

    def sort(self, key=lambda x: x[0], reverse=False):
        sorted_list = sorted(self.list, key=key, reverse=reverse)
        return sorted_list

    def calculate_delta(self, start_val, end_val, start_date, end_date):
        time_delta = self.list[end_date] - self.list[start_date]
        weight = self.list[start_val] - self.list[end_val]
        if weight <= 0:
            delta = weight / time_delta.days
        else:
            delta = -(weight / time_delta.days)
        return delta

    def calculate_net_change(self, start_val, end_val):
        net_change = abs(self.list[start_val] - self.list[end_val])
        return net_change

    def calculate_time_to_goal(self, start_val, goal_val, delta):
        diff = self.list[start_val] - goal_val
        days = abs(int(diff / delta))
        end_date = DATETODAY + datetime.timedelta(days=days)
        return days, end_date


class LiftHistory(WeightHistory):
    """Define"""

    def __init__(self, lift, lift_list=None):
        super().__init__(lift_list)
        self.lift = lift
        self.list = lift_list

    def __str__(self):
        return f'(Lift: {self.lift}| Lift History: {self.list})'

    def __repr__(self):
        return f'{__class__.__name__}({self.lift}, {self.list})'


class DateEntry:
    """Define"""

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def date_validation(self):
        """Validates date parameter if it matches ISO format and raises ValueError if it does not."""
        date = '-'.join((self.year, self.month, self.day))
        try:
            date_obj = datetime.date.strftime(date, '%Y-%m-%d')
        except ValueError:
            logger.exception('Value error raised.')
            raise ValueError
        else:
            return date_obj
