import datetime

DATETODAY = datetime.date.today()


def calculate_percentage_of_1_rep_max(weight, reps):
    one_rep_max = weight / (1.0278 - 0.0278 * reps)
    percentage = weight / one_rep_max
    return percentage, one_rep_max


def calculate_volume(weight, reps):
    volume = weight * reps
    return volume


def average_rpe(sets):
    average = (sum(obj.getattr(obj, 'rpe', 0) for obj in sets) / len(sets))
    return average


def calculate_total_reps(sets):
    total = sum(obj.getattr(obj, 'reps', 0) for obj in sets)
    return total


def calculate_total_volume(sets):
    volume = sum(obj.getattr(obj, 'volume', 0) for obj in sets)
    return volume


def sort(ilist, key=lambda x: x[0], reverse=False):
    sorted_list = sorted(ilist, key=key, reverse=reverse)
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
