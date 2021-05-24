import datetime

from AlarmCalendar import *
from documents.rw_dict import *

myCalendar = AlarmCalendar()
my_calendars = read_dict_file('documents/my_calendars.txt')


def test_alarm():
    myCalendar.set_calendars(alarm_calendar=my_calendars['Reveil'],
                             public_holiday_calendar=my_calendars['Jours Feries'],
                             personal_calendar=my_calendars['Elise et Tom'])

    date1 = datetime.datetime(2020, 3, 24)
    is_alarm1, event1 = myCalendar.is_alarm_today(date1)
    assert len(is_alarm1) == 0
    assert len(event1) == 0

    date2 = datetime.datetime(2020, 3, 25)
    is_alarm2, event2 = myCalendar.is_alarm_today(date2)
    assert is_alarm2[0] is True
    assert event2[0].title == 'Reveil 1'

    date3 = datetime.datetime(2020, 3, 26)
    is_alarm3, event3 = myCalendar.is_alarm_today(date3)
    assert is_alarm3[0] is True
    assert event3[0].title == '#force Reveil 2'

    date4 = datetime.datetime(2020, 3, 27)
    is_alarm4, event4 = myCalendar.is_alarm_today(date4)
    assert is_alarm4[0] is False
    assert event4[0].title == '#off congé 1'

    date5 = datetime.datetime(2020, 3, 28)
    is_alarm5, event5 = myCalendar.is_alarm_today(date5)
    assert is_alarm5[0] is False
    assert event5[0].title == 'congé 2'

    date6 = datetime.datetime(2020, 3, 29)
    is_alarm6, event6 = myCalendar.is_alarm_today(date6)
    assert is_alarm6[0] is False
    assert event6[0].title == 'Heure d\'été'

    date7 = datetime.datetime(2020, 4, 2)
    is_alarm7, event7 = myCalendar.is_alarm_today(date7)
    assert is_alarm7[0] is True
    assert event7[0].title == '#FORCE Reveil 3'

    date8 = datetime.datetime(2020, 4, 3)
    is_alarm8, event8 = myCalendar.is_alarm_today(date8)
    assert is_alarm8[0] is False
    assert event8[0].title == '#OFF Congé 3'
