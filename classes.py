import logging
import datetime

logger = logging.getLogger(__name__)

TODAY = datetime.date.today()


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
        try:
            date = datetime.date.strftime(date, '%Y-%m-%d')
        except ValueError:
            logger.exception('Value error raised.')
            raise ValueError
        return date

    @staticmethod
    def value_validation(value):
        if not (isinstance(value, int) or isinstance(value, float)):
            logger.exception('Type error raised.')
            raise TypeError
        else:
            return value


class LiftEntry(WeightEntry):
    """Define"""

    def __init__(self, date, weight, reps):
        super().__init__(date, weight)
        self.date = date
        self.weight = weight
        self.reps = reps
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

    @staticmethod
    def calculate_total_volume(*args):
        total_volume = sum(x for x in args)
        return total_volume


class WeightHistory:
    """Define"""

    def __init__(self, weight_list=None):
        self.list = weight_list

    def __str__(self):
        return f'(Weight History: {self.list})'

    def __repr__(self):
        return f'{__class__.__name__}({self.list})'

    def sort(self, reverse=False):
        sorted_list = sorted(self.list, key=lambda x: x[0], reverse=reverse)
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
        pass


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
