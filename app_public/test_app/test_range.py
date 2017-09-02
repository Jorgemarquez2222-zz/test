from datetime import datetime, timedelta
from django.test import TestCase
from app_public.app.range import Range
from app_public.models import Appointment


class TestRange(TestCase):
    def setUp(self):
        self.start = datetime(2016, 12, 12, 10, 30)
        self.end = datetime(2016, 12, 12, 11, 0)
        self.range = Range(self.start, self.end)

    def test_sub_appointment(self):
        appointment = Appointment()
        appointment.start = self.start
        appointment.end = self.end
        available_ranges = self.range.__sub__(appointment)
        self.assertEqual(0, len(available_ranges))
        duration = self.range.get_duration()
        appointment.start = self.range.start + duration * 2
        appointment.end = self.range.end + duration * 2
        available_ranges = self.range.__sub__(appointment)
        self.assertEqual(1, len(available_ranges))
        self.assertTrue(self.range == available_ranges[0])
        appointment.start = self.range.start - timedelta(minutes=30)
        appointment.end = self.range.end - timedelta(minutes=15)
        available_ranges = self.range.__sub__(appointment)
        self.assertEqual(1, len(available_ranges))
        self.assertTrue(Range(appointment.end, self.end) == available_ranges[0])
        appointment.start = self.range.start + timedelta(minutes=5)
        appointment.end = self.range.end + timedelta(minutes=5)
        available_ranges = self.range.__sub__(appointment)
        self.assertEqual(1, len(available_ranges))
        self.assertTrue(Range(self.start, appointment.start) == available_ranges[0])
        appointment.start = self.range.start + timedelta(minutes=5)
        appointment.end = self.range.end + timedelta(minutes=-5)
        available_ranges = self.range.__sub__(appointment)
        self.assertEqual(2, len(available_ranges))
        self.assertTrue(Range(self.start, appointment.start) == available_ranges[0])
        self.assertTrue(Range(appointment.end, self.end) == available_ranges[1])

    def test_intersects(self):
        intersecting_range = Range(self.range.start + timedelta(minutes=10), self.range.end + timedelta(minutes=10))
        self.assertTrue(self.range.intersects(intersecting_range))
        duration = self.range.get_duration()
        not_intersecting_range = Range(self.range.start + duration * 2, self.range.end + duration * 2)
        self.assertFalse(self.range.intersects(not_intersecting_range))

    def test_contains(self):
        contained_range = Range(self.range.start + timedelta(minutes=10), self.range.end + timedelta(minutes=-10))
        self.assertTrue(self.range.contains(contained_range))
        not_contained_range = Range(self.range.start + timedelta(minutes=-10), self.range.end + timedelta(minutes=10))
        self.assertFalse(self.range.contains(not_contained_range))

    def test_get_data(self):
        range_data = self.range.get_dict()
        self.assertEqual(self.start, range_data['start'])
        self.assertEqual(self.end, range_data['end'])
