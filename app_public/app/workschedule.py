#from datetime import timedelta
#
#from app_public.models import WorkScheduleSlot, WorkScheduleGroup, AvailableSlot
#
#"""
#    Takes a string with app types ids separated by ;
#    Ex : "2;5;10;"
#    And returns the list of AppointmentType
#"""
#def parse_appointment_types(doctor, appointment_types):
#    l = []
#    app_types = doctor.appointment_types.all()
#
#    for appid in appointment_types.split(';'):
#        if appid != '':
#            l.append(app_types.get(id=appid))
#
#    return l
#
#"""
#    Creates a WorkSchedule for a doctor and adds disponible doctor slots
#    Creating recursive slots while end <= recursion_end (with 7 days interval)
#        appointment_types : list or queryset of AppointmentType models
#"""
#def create_workschedule(doctor, start, end, appointment_types=None, name=None, recurrent=False, recursion_end=None):
#    """
#        test if overlapping work slots
#        create ws
#        add all occurences to available slots for doctor
#    """
#    wsg = WorkScheduleGroup(name=name, doctor=doctor)
#    wsg.save()
#
#    if not appointment_types is None:
#        for appt in appointment_types:
#            wsg.appointment_types.add(appt)
            #
#    wss = WorkScheduleSlot(work_schedule_group=wsg, start=start, end=end)
#    wss.save()
#    AvailableSlot(work_schedule_slot=wss, start=start, end=end).save()
#
#    if recurrent and recursion_end is not None:
#        start = start + timedelta(days=7)
#        end = end + timedelta(days=7)
#        while end <= recursion_end:
#            wss = WorkScheduleSlot(work_schedule_group=wsg, start=start, end=end)
#            wss.save()
#            AvailableSlot(work_schedule_slot=wss, start=start, end=end).save()
#            start = start + timedelta(days=7)
#            end = end + timedelta(days=7)
#
#    return wsg
#
#"""
#	Removes a work schedule
#"""
#def remove_workschedule(id, remove_all_occurences=False):
#    ws = WorkScheduleSlot.objects.get(id=id)
#
#    if remove_all_occurences:
#        for wss in ws.work_schedule_group.work_schedule_slots.all():
#            for avs in wss.available_slots.all():
#                avs.delete()
#        ws.work_schedule_group.delete()
#    else:
#        for avs in ws.available_slots.all():
#            avs.delete()
#        ws.delete()