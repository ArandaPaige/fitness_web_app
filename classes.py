class User:
    """Define"""

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __str__(self):
        return f'({self.user_id}, {self.name})'

    def __repr__(self):
        return f'{__class__.__name__}({self.user_id}, {self.name})'


class WeightEntry:
    """Define"""

    def __init__(self, weight, date):
        self.weight = weight
        self.date = date
        self.collection = ()

    def __str__(self):
        return f'{self.weight}, {self.date}'

    def __repr__(self):
        return f'{__class__.__name__}({self.weight}, {self.date}'


class WeightHistory:
    """Define"""

    def __init__(self, weight_list=None):
        self.list = weight_list

    def __str__(self):
        return f'({self.list})'

    def __repr__(self):
        return f'{__class__.__name__}({self.list})'

    def sort(self):
        sorted_list = sorted(self.list)
        return sorted_list

    def calculate_delta(self, start_date, end_date):
        pass

    def calculate_net_change(self, entry1, entry2):
        pass


class LiftEntry(WeightEntry):
    """Define"""

    def __init__(self, date, sets, reps):
        super().__init__(sets, reps)
        self.date = date
        self.sets = sets
        self.reps = reps
        self.collection = ()

    def __str__(self):
        return f'({self.date}, {self.sets}, {self.reps})'

    def __repr__(self):
        return f'{__class__.__name__}({self.date}, {self.sets}, {self.reps})'

    def calculate_volume(self):
        volume = self.sets * self.reps
        return volume


class LiftHistory(WeightHistory):
    """Define"""

    def __init__(self, lift, lift_list=None):
        super().__init__(lift)
        self.lift = lift
        self.list = lift_list

    def __str__(self):
        return f'({self.lift})'

    def __repr__(self):
        return f'{__class__.__name__}({self.lift})'

