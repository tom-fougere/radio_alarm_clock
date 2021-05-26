import datetime

from AlarmCalendar import *
from documents.rw_dict import *

myCalendar = OnlineCalendar()
my_calendars = read_dict_file('documents/my_calendars.txt')

alarm_calendar_name = 'Alarm'
public_holiday_calendar_name = 'Public Holiday'
personal_calendar_name = 'Personal'

myCalendar.set_calendars(alarm_calendar=my_calendars['Reveil'],
                         public_holiday_calendar=my_calendars['Jours Feries'],
                         personal_calendar=my_calendars['Elise et Tom'])

def test_get_events():

    date1 = datetime.datetime(2020, 3, 24)
    events1 = myCalendar.get_events(date1)
    assert len(events1) == 3
    assert (events1[0].kind == 'None' and events1[0].name == public_holiday_calendar_name)
    assert (events1[1].kind == 'None' and events1[1].name == alarm_calendar_name)
    assert (events1[2].kind == 'None' and events1[2].name == personal_calendar_name)

    date2 = datetime.datetime(2020, 3, 25)
    events2 = myCalendar.get_events(date2)
    assert len(events2) == 3
    assert events2[0].title == 'Reveil 1'
    assert (events2[1].kind == 'None' and events2[1].name == public_holiday_calendar_name)
    assert (events2[2].kind == 'None' and events2[2].name == personal_calendar_name)

    date3 = datetime.datetime(2020, 3, 27)
    events3 = myCalendar.get_events(date3)
    assert len(events3) == 3
    assert events3[0].title == '#off congé 1'
    assert (events3[1].kind == 'None' and events3[1].name == public_holiday_calendar_name)
    assert (events3[2].kind == 'None' and events3[2].name == alarm_calendar_name)

    date4 = datetime.datetime(2020, 3, 29)
    events4 = myCalendar.get_events(date4)
    assert len(events4) == 3
    assert events4[0].title == 'Heure d\'été'
    assert (events4[1].kind == 'None' and events4[1].name == alarm_calendar_name)
    assert (events4[2].kind == 'None' and events4[2].name == personal_calendar_name)

    date5 = datetime.datetime(2020, 4, 2)
    events5 = myCalendar.get_events(date5)
    assert len(events5) == 3
    assert events5[0].title == '#FORCE Reveil 3'
    assert events5[1].title == '#OFF Congé 3'
    assert (events5[2].kind == 'None' and events5[2].name == public_holiday_calendar_name)

    date6 = datetime.datetime(2020, 4, 4)
    events6 = myCalendar.get_events(date6)
    assert len(events6) == 5
    assert events6[0].title == '#force reveil'
    assert events6[1].title == '#off vac'
    assert events6[2].title == 'reveil pas force'
    assert events6[3].title == 'rdv'
    assert (events6[4].kind == 'None' and events6[4].name == public_holiday_calendar_name)


def test_alarm():

    date1 = datetime.datetime(2020, 3, 24)
    is_alarm1, event1 = myCalendar.is_alarm_today(date1)
    assert is_alarm1 is False
    assert event1.kind == 'None'

    date2 = datetime.datetime(2020, 3, 25)
    is_alarm2, event2 = myCalendar.is_alarm_today(date2)
    assert is_alarm2 is True
    assert event2.title == 'Reveil 1'

    date3 = datetime.datetime(2020, 3, 26)
    is_alarm3, event3 = myCalendar.is_alarm_today(date3)
    assert is_alarm3 is True
    assert event3.title == '#force Reveil 2'

    date4 = datetime.datetime(2020, 3, 27)
    is_alarm4, event4 = myCalendar.is_alarm_today(date4)
    assert is_alarm4 is False
    assert event4.title == '#off congé 1'

    date5 = datetime.datetime(2020, 3, 28)
    is_alarm5, event5 = myCalendar.is_alarm_today(date5)
    assert is_alarm5 is False
    assert event5.title == 'congé 2'

    date6 = datetime.datetime(2020, 3, 29)
    is_alarm6, event6 = myCalendar.is_alarm_today(date6)
    assert is_alarm6 is False
    assert event6.title == 'Heure d\'été'

    date7 = datetime.datetime(2020, 4, 2)
    is_alarm7, event7 = myCalendar.is_alarm_today(date7)
    assert is_alarm7 is True
    assert event7.title == '#FORCE Reveil 3'

    date8 = datetime.datetime(2020, 4, 3)
    is_alarm8, event8 = myCalendar.is_alarm_today(date8)
    assert is_alarm8 is False
    assert event8.title == '#OFF Congé 3'

    date9 = datetime.datetime(2020, 4, 4)
    is_alarm9, event9 = myCalendar.is_alarm_today(date9)
    assert is_alarm9 is True
    assert event9.title == '#force reveil'

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

