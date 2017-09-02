import datetime
from typing import List
from django.db.models import Q

from app_public.models import Doctor, AppointmentType, Appointment, AvailableSlot, WorkSchedule

from app_public.app.range import Range


"""
    Tests if date corresponds to a precise time interval from ref
        ref : starting datetime
        date : datetime to test
        granularity : time interval
"""


def is_on_granularity(ref: datetime.datetime, date: datetime.datetime, granularity: datetime.timedelta) -> bool:
    d = ref

    while d <= date:
        if d == date:
            return True
        d += granularity

    return False


"""
    Tests if the appointment is on an available slot
"""


def is_on_available_slot(doctor : Doctor, start : datetime.datetime, end : datetime.datetime) -> bool:
    return AvailableSlot.objects.filter(work_schedule_slot__work_schedule_group__doctor=doctor,
                                        start__lte=start,
                                        end__gte=end).exists()


"""
    Returns available slots between start and end
"""


def get_available_slots_in(doctor : Doctor, start : datetime.datetime, end : datetime.datetime) -> List[AvailableSlot]:
    return AvailableSlot.objects.filter(work_schedule_slot__work_schedule_group__doctor=doctor,
                                        start__gte=start,
                                        end__lte=end)


"""
    Returns available slot that intersects with start and end
"""


def get_available_slot_for(doctor : Doctor, start : datetime.datetime, end : datetime.datetime) -> List[AvailableSlot]:
    return AvailableSlot.objects.get(work_schedule_slot__work_schedule_group__doctor=doctor,
                                         start__lte=end,
                                         end__gte=start)


"""
    Tests if the appointment is on an available time
    For the patients that can only take appointments on defined times
"""


def is_available_appointment(doctor : Doctor, start : datetime.datetime, appointment_type : AppointmentType) -> bool:
    end = start + appointment_type.duration
    slots = AvailableSlot.objects.filter(work_schedule_slot__work_schedule_group__doctor=doctor,
                                         start__lte=start,
                                         end__gte=end)

    if not slots.exists():
        return False

    for s in slots:
        granularity = s.work_schedule_slot.get_granularity()
        if is_on_granularity(s.start, start, granularity) and end <= s.end:
            return True

    return False


"""
    Converts AvailableSlots to list of available appointments times
"""


def available_slots_to_appointments_granularized(slots : List[AvailableSlot]) -> List[datetime.datetime]:
    apps = []
    for slot in slots:
        gran = slot.work_schedule_slot.get_granularity()
        time = slot.start
        while time + gran <= slot.end:
            apps.append(time)
            time += gran
    return apps


"""
    Returns the list of the datetimes where the patient can take appointment
"""


def get_available_appointment_granularized(doctor : Doctor, start : datetime.datetime, end: datetime.datetime) -> List[datetime.datetime]:
    slots = get_available_slots_in(doctor, start, end)
    app_dates = available_slots_to_appointments_granularized(slots)
    return app_dates


"""
    Makes the slots between start and end used
"""


def make_available_slot_used(doctor, start, end):
    query = AvailableSlot.objects.filter(work_schedule_slot__work_schedule_group__doctor=doctor,
                                        start__lte=end,
                                        end__gte=start)

    app_range = Range(start, end)

    for slot in query:
        slot_range = Range(slot.start, slot.end)
        wss = slot.work_schedule_slot
    
        slot.delete()
        left = slot_range - app_range

        for r in left:
            AvailableSlot(work_schedule_slot=wss, start=r.start, end=r.end).save()


"""
    Merges adjacent free slots in a work schedule
"""


def merge_available_slots(wss):
    avs = wss.available_slots.all().order_by('start')
    l = len(avs)
    i = 0

    while i < l - 1:
        if avs[i + 1].start <= avs[i].end:
            avs[i].end = avs[i + 1].end
            avs[i].save()
            avs[i + 1].delete()
            i = l
            merge_available_slots(wss)
        else:
            i += 1


"""
    Makes the slots between start and end free
"""


def make_available_slot_free(doctor, start, end):
    wsss = WorkScheduleSlot.objects.filter(work_schedule_group__doctor=doctor,
                                        start__lte=end,
                                        end__gte=start)
    
    for wss in wsss:
        new_as = AvailableSlot(work_schedule_slot=wss, start=start, end=end)
        new_as.save()
        wss.available_slots.add(new_as)
        merge_available_slots(wss)


"""
    Creates the appointment
    Updates available slots
"""


def create_appointment(doctor, patient, start, end=None, appointment_type=None, name=None, comment=None):
    if end is None and appointment_type is None:
        raise Exception('Can not create appointment, end and app type None')
    if end is None:
        end = start + appointment_type.duration
    if name is None:
        name = ""
    if comment is None:
        comment = ""

    new_app = Appointment(doctor=doctor,
        patient=patient,
        appointment_type=appointment_type,
        start=start,
        end=end,
        name=name,
        comment=comment)
    new_app.save()
    make_available_slot_used(doctor, start, end)

    return new_app


"""
    Removes the appointment
    Updates available slots
    Raise an error if my_user is not in the appointment
"""


def remove_appointment(appointment_id, my_user):
    app = Appointment.objects.get(Q(id=appointment_id) & (Q(patient=my_user) | Q(doctor=my_user)))
    make_available_slot_free(app.doctor, app.start, app.end)
    app.delete()