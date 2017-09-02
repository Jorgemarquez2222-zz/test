from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase

import app_public.app.appointments as underTest
from app_public.models import AvailableSlot, MyUser, Doctor, WorkScheduleSlot, AppointmentType, WorkScheduleGroup


class TestAvailability(TestCase):
    def setUp(self):
        self.underTest = underTest

    def test_is_on_granularity(self):
        reference_date_time = datetime(2016, 12, 12, 10, 30)
        test_date_time = datetime(2016, 12, 12, 11, 30)
        test_granularity = timedelta(minutes=30)
        self.assertTrue(self.underTest.is_on_granularity(reference_date_time, test_date_time, test_granularity))
        test_date_time = datetime(2016, 12, 12, 11, 45)
        test_granularity = timedelta(minutes=30)
        self.assertFalse(self.underTest.is_on_granularity(reference_date_time, test_date_time, test_granularity))

    def test_is_on_available_slot(self):
        user_doctor = User.objects.create_user('chapatin', 'dcchapatin@chespitiro.com', 'medacosas')
        user_doctor.save()
        my_user_doctor = MyUser(user=user_doctor)
        my_user_doctor.save()
        test_doctor = Doctor(myuser_ptr_id=my_user_doctor.pk)
        test_doctor.__dict__.update(my_user_doctor.__dict__)
        test_doctor.save()
        test_appointment_type = AppointmentType()
        test_appointment_type.duration = timedelta(minutes=30)
        test_appointment_type.save()
        test_work_schedule_group = WorkScheduleGroup()
        test_work_schedule_group.doctor = test_doctor
        test_work_schedule_group.save()
        test_work_schedule_group.appointment_types.add(test_appointment_type)
        test_work_schedule_slot = WorkScheduleSlot()
        test_work_schedule_slot.work_schedule_group = test_work_schedule_group
        test_work_schedule_slot.start = datetime(2016, 6, 8, 12, 0)
        test_work_schedule_slot.end = datetime(2016, 6, 8, 18, 0)
        test_work_schedule_slot.save()
        test_available_slot = AvailableSlot()
        test_available_slot.work_schedule_slot = test_work_schedule_slot
        test_available_slot.start = datetime(2016, 6, 8, 12, 0)
        test_available_slot.end = datetime(2016, 6, 8, 13, 0)
        test_available_slot.save()
        appointment_start_time = datetime(2016, 6, 8, 12, 0)
        appointment_end_time = datetime(2016, 6, 8, 12, 30)
        self.assertTrue(self.underTest.is_on_available_slot(test_doctor, appointment_start_time, appointment_end_time))
        appointment_start_time = datetime(2016, 6, 8, 12, 0)
        appointment_end_time = datetime(2016, 6, 8, 14, 30)
        self.assertFalse(self.underTest.is_on_available_slot(test_doctor, appointment_start_time, appointment_end_time))

    def test_is_available_appointment(self):
        user_doctor = User.objects.create_user('chapatin', 'dcchapatin@chespitiro.com', 'medacosas')
        user_doctor.save()
        my_user_doctor = MyUser(user=user_doctor)
        my_user_doctor.save()
        test_doctor = Doctor(myuser_ptr_id=my_user_doctor.pk)
        test_doctor.__dict__.update(my_user_doctor.__dict__)
        test_doctor.save()
        test_appointment_type = AppointmentType()
        test_appointment_type.duration = timedelta(minutes=30)
        test_appointment_type.save()
        test_work_schedule_group = WorkScheduleGroup()
        test_work_schedule_group.doctor = test_doctor
        test_work_schedule_group.save()
        test_work_schedule_group.appointment_types.add(test_appointment_type)
        test_work_schedule_slot = WorkScheduleSlot()
        test_work_schedule_slot.work_schedule_group = test_work_schedule_group
        test_work_schedule_slot.start = datetime(2016, 6, 8, 12, 0)
        test_work_schedule_slot.end = datetime(2016, 6, 8, 18, 0)
        test_work_schedule_slot.save()
        test_available_slot = AvailableSlot()
        test_available_slot.work_schedule_slot = test_work_schedule_slot
        test_available_slot.start = datetime(2016, 6, 8, 12, 0)
        test_available_slot.end = datetime(2016, 6, 8, 13, 0)
        test_available_slot.save()
        appointment_start_time = timezone.make_aware(datetime(2016, 6, 8, 12, 0), timezone.get_default_timezone())
        test_appointment_type = AppointmentType()
        test_appointment_type.duration = timedelta(minutes=30)
        self.assertTrue(self.underTest.is_available_appointment(test_doctor, appointment_start_time, test_appointment_type))
        test_appointment_type.duration = timedelta(minutes=90) # this appointment is too long
        self.assertFalse(self.underTest.is_available_appointment(test_doctor, appointment_start_time, test_appointment_type))

    def test_get_available_slots(self):
        user_doctor = User.objects.create_user('chapatin', 'dcchapatin@chespitiro.com', 'medacosas')
        user_doctor.save()
        my_user_doctor = MyUser(user=user_doctor)
        my_user_doctor.save()
        test_doctor = Doctor(myuser_ptr_id=my_user_doctor.pk)
        test_doctor.__dict__.update(my_user_doctor.__dict__)
        test_doctor.save()
        test_appointment_type = AppointmentType()
        test_appointment_type.duration = timedelta(minutes=30)
        test_appointment_type.save()
        test_work_schedule_group = WorkScheduleGroup()
        test_work_schedule_group.doctor = test_doctor
        test_work_schedule_group.save()
        test_work_schedule_group.appointment_types.add(test_appointment_type)
        test_work_schedule_slot = WorkScheduleSlot()
        test_work_schedule_slot.work_schedule_group = test_work_schedule_group
        test_work_schedule_slot.start = datetime(2016, 6, 8, 12, 0)
        test_work_schedule_slot.end = datetime(2016, 6, 8, 18, 0)
        test_work_schedule_slot.save()
        test_available_slot = AvailableSlot()
        test_available_slot.work_schedule_slot = test_work_schedule_slot
        test_available_slot.start = datetime(2016, 6, 8, 12, 0)
        test_available_slot.end = datetime(2016, 6, 8, 13, 0)
        test_available_slot.save()
        available_slots = self.underTest.get_available_slots(test_doctor, datetime(2016, 6, 8, 12, 0), datetime(2016, 6, 8, 15, 0))
        self.assertTrue(available_slots.count() == 1)
        available_slots = self.underTest.get_available_slots(test_doctor, datetime(2016, 6, 8, 13, 0), datetime(2016, 6, 8, 15, 0))
        self.assertTrue(available_slots.count() == 0)

    def test_slot_to_appointments(self):
        user_doctor = User.objects.create_user('chapatin', 'dcchapatin@chespitiro.com', 'medacosas')
        user_doctor.save()
        my_user_doctor = MyUser(user=user_doctor)
        my_user_doctor.save()
        test_doctor = Doctor(myuser_ptr_id=my_user_doctor.pk)
        test_doctor.__dict__.update(my_user_doctor.__dict__)
        test_doctor.save()
        test_appointment_type = AppointmentType()
        test_appointment_type.duration = timedelta(minutes=30)
        test_appointment_type.save()
        test_work_schedule_group = WorkScheduleGroup()
        test_work_schedule_group.doctor = test_doctor
        test_work_schedule_group.save()
        test_work_schedule_group.appointment_types.add(test_appointment_type)
        test_work_schedule_slot = WorkScheduleSlot()
        test_work_schedule_slot.work_schedule_group = test_work_schedule_group
        test_work_schedule_slot.start = datetime(2016, 6, 8, 12, 0)
        test_work_schedule_slot.end = datetime(2016, 6, 8, 18, 0)
        test_work_schedule_slot.save()
        test_available_slot = AvailableSlot()
        test_available_slot.work_schedule_slot = test_work_schedule_slot
        test_available_slot.start = datetime(2016, 6, 8, 12, 0)
        test_available_slot.end = datetime(2016, 6, 8, 13, 0)
        test_available_slot.save()
        available_slots = self.underTest.get_available_slots(test_doctor, datetime(2016, 6, 8, 12, 0), datetime(2016, 6, 8, 15, 0))
        appointments = self.underTest.slot_to_appointments(available_slots)
        self.assertEqual(2, len(appointments))

    def test_get_available_appointment_times(self):
        user_doctor = User.objects.create_user('chapatin', 'dcchapatin@chespitiro.com', 'medacosas')
        user_doctor.save()
        my_user_doctor = MyUser(user=user_doctor)
        my_user_doctor.save()
        test_doctor = Doctor(myuser_ptr_id=my_user_doctor.pk)
        test_doctor.__dict__.update(my_user_doctor.__dict__)
        test_doctor.save()
        test_appointment_type = AppointmentType()
        test_appointment_type.duration = timedelta(minutes=30)
        test_appointment_type.save()
        test_work_schedule_group = WorkScheduleGroup()
        test_work_schedule_group.doctor = test_doctor
        test_work_schedule_group.save()
        test_work_schedule_group.appointment_types.add(test_appointment_type)
        test_work_schedule_slot = WorkScheduleSlot()
        test_work_schedule_slot.work_schedule_group = test_work_schedule_group
        test_work_schedule_slot.start = datetime(2016, 6, 8, 12, 0)
        test_work_schedule_slot.end = datetime(2016, 6, 8, 18, 0)
        test_work_schedule_slot.save()
        test_available_slot = AvailableSlot()
        test_available_slot.work_schedule_slot = test_work_schedule_slot
        test_available_slot.start = datetime(2016, 6, 8, 12, 0)
        test_available_slot.end = datetime(2016, 6, 8, 13, 0)
        test_available_slot.save()
        appointments = self.underTest.get_available_appointment_times(test_doctor, datetime(2016, 6, 8, 12, 0), datetime(2016, 6, 8, 15, 0))
        self.assertEqual(2, len(appointments))