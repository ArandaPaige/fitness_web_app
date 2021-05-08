import unittest
import datetime
from classes import User, WeightEntry, DateEntry, SetEntry

DATETODAY = datetime.date.today()


class TestUser(unittest.TestCase):
    def test_username_validation(self):
        self.assertEqual(True, False)

    def test_email_validation(self):
        self.assertEqual(True, False)

    def test_password_validation(self):
        self.assertEqual(True, False)


class TestWeightEntry(unittest.TestCase):
    def setUp(self):
        self.weight_entry1 = WeightEntry(150)
        self.weight_entry2 = WeightEntry(165, date=(DATETODAY - datetime.timedelta(days=5)))

    def test_sort(self):
        self.assertEqual(True, False)

    def test_calculate_net_change(self):
        net_change = WeightEntry.calculate_net_change()
        self.assertEqual(net_change, 15)

    def test_calculate_delta(self):
        self.assertEqual(True, False)

    def test_calculate_time_to_goal(self):
        self.assertEqual(True, False)


class TestSetEntry(unittest.TestCase):
    def setUp(self):
        self.set_entry1 = SetEntry('Squat', 225, 10, 6)
        self.set_entry2 = SetEntry('Squat', 300, 10, 9)

    def test_volume(self):
        self.assertEqual(2250, self.set_entry1.volume)

    def test_calculate_percentage_one_1_rep_max(self):
        percentage, one_rep_max = self.set_entry2.calculate_percentage_of_1_rep_max()
        self.assertEqual((percentage, one_rep_max), ())

    def test_average_rpe(self):
        average_rpe = SetEntry.average_rpe((self.set_entry1, self.set_entry2))
        self.assertEqual(average_rpe, 7.5)

    def test_calculate_total_reps(self):
        total_reps = SetEntry.calculate_total_reps((self.set_entry1, self.set_entry2))
        self.assertEqual(total_reps, 20)

    def test_calculate_total_volume(self):
        total_volume = SetEntry.calculate_total_volume((self.set_entry1, self.set_entry2))
        self.assertEqual(total_volume, 5250)


class TestDateEntry(unittest.TestCase):
    def test_date_validation(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
