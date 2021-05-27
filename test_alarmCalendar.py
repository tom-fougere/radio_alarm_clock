import datetime

from AlarmCalendar import *
from documents.rw_dict import *

myCalendar = OnlineCalendar()
my_calendars = read_dict_file('documents/my_calendars.txt')

myCalendar.set_calendars(alarm_calendar=my_calendars['Reveil'],
                         public_holiday_calendar=my_calendars['Jours Feries'],
                         personal_calendar=my_calendars['Elise et Tom'])

def test_get_events():

    date1 = datetime.datetime(2020, 3, 24)
    events1 = myCalendar.get_events(date1)
    assert len(events1) == 3
    assert (events1[0].kind == 'None' and events1[0].is_alarm == False)
    assert (events1[1].kind == 'None' and events1[1].is_alarm == False)
    assert (events1[2].kind == 'None' and events1[2].is_alarm == False)

    date2 = datetime.datetime(2020, 3, 25)
    events2 = myCalendar.get_events(date2)
    assert len(events2) == 3
    assert (events2[0].title == 'Reveil 1' and events2[0].is_alarm == True)
    assert (events2[1].kind == 'None' and events2[1].is_alarm == False)
    assert (events2[2].kind == 'None' and events2[2].is_alarm == False)

    date3 = datetime.datetime(2020, 3, 27)
    events3 = myCalendar.get_events(date3)
    assert len(events3) == 3
    assert (events3[0].title == '#off congé 1' and events3[0].is_alarm == False)
    assert (events3[1].kind == 'None' and events3[1].is_alarm == False)
    assert (events3[2].kind == 'None' and events3[2].is_alarm == False)

    date4 = datetime.datetime(2020, 3, 29)
    events4 = myCalendar.get_events(date4)
    assert len(events4) == 3
    assert (events4[0].title == 'Heure d\'été' and events4[0].is_alarm == False)
    assert (events4[1].kind == 'None' and events4[1].is_alarm == False)
    assert (events4[2].kind == 'None' and events4[2].is_alarm == False)

    date5 = datetime.datetime(2020, 4, 2)
    events5 = myCalendar.get_events(date5)
    assert len(events5) == 3
    assert (events5[0].title == '#FORCE Reveil 3' and events5[0].is_alarm == True)
    assert (events5[1].title == '#OFF Congé 3' and events5[1].is_alarm == False)
    assert (events5[2].kind == 'None' and events5[2].is_alarm == False)

    date6 = datetime.datetime(2020, 4, 4)
    events6 = myCalendar.get_events(date6)
    assert len(events6) == 5
    assert (events6[0].title == '#force reveil' and events6[0].is_alarm == True)
    assert (events6[1].title == '#off vac' and events6[1].is_alarm == False)
    assert (events6[2].title == 'reveil pas force' and events6[2].is_alarm == True)
    assert (events6[3].title == 'rdv' and events6[3].is_alarm == False)
    assert (events6[4].kind == 'None' and events6[4].is_alarm == False)

def test_force_alarm():

    date1 = datetime.datetime(2020, 3, 16)

    events_before = myCalendar.google_service.get_events_from_day(my_calendars['Reveil'], date1, reset_hour=True)
    text_before = events_before['items'][0]['summary']

    myCalendar.force_alarm(date1)

    events_after = myCalendar.google_service.get_events_from_day(my_calendars['Reveil'], date1, reset_hour=True)
    text_after = events_after['items'][0]['summary']

    assert ' '.join(['#force', text_before]) == text_after

    # Remove the added text
    myCalendar.google_service.update_event(events_before['items'][0], my_calendars['Reveil'])

