from events import Event
from AlarmCalendar import *
from documents.rw_dict import *

myCalendar = AlarmCalendar()    # Init state
my_calendars = read_dict_file('documents/my_calendars.txt')
myCalendar.set_calendars(alarm_calendar=my_calendars['Reveil'],
                         public_holiday_calendar=my_calendars['Jours Feries'],
                         personal_calendar=my_calendars['Elise et Tom'])

my_event = Event()


def setup_function():
    my_event.clear_event()


def test_event():

    # First day
    one_date = datetime.datetime(2020, 3, 30)
    is_alarm, events = myCalendar.is_alarm_today(one_date)

    my_event.set_event(is_alarm, events)

    assert my_event.is_alarm is True
    assert my_event.title == 'essai1'
    assert my_event.start_time == datetime.datetime(2020, 3, 30, hour=9, minute=30)
    assert my_event.end_time == datetime.datetime(2020, 3, 30, hour=10, minute=30)
    assert my_event.radio == 'nrj'  # default value
    assert my_event.repetition == 10  # default value

    # Second day
    one_date = datetime.datetime(2020, 3, 31)
    is_alarm, events = myCalendar.is_alarm_today(one_date)

    my_event.set_event(is_alarm, events)

    assert my_event.is_alarm is True
    assert my_event.title == 'essai2'
    assert my_event.start_time == datetime.datetime(2020, 3, 31, hour=12, minute=00)
    assert my_event.end_time == datetime.datetime(2020, 3, 31, hour=13, minute=00)
    assert my_event.radio == 'nrj'  # default value
    assert my_event.repetition == 10  # default value

    # Third day
    one_date = datetime.datetime(2020, 4, 1)
    is_alarm, events = myCalendar.is_alarm_today(one_date)

    my_event.set_event(is_alarm, events)

    assert my_event.is_alarm is True
    assert my_event.title == 'essai3'
    assert my_event.start_time == datetime.datetime(2020, 4, 1, hour=15, minute=30)
    assert my_event.end_time == datetime.datetime(2020, 4, 1, hour=16, minute=30)
    assert my_event.radio == 'fun'
    assert my_event.repetition == 15


def test_list_of_alarms():

    # First day
    one_date = datetime.datetime(2020, 3, 30)
    is_alarm, events = myCalendar.is_alarm_today(one_date)

    my_event.set_event(is_alarm, events)

    alarms = [datetime.datetime(2020, 3, 30, hour=9, minute=30),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=10),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=20),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=30),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=40),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=50)]

    assert len(my_event.alarms) == 6
    assert all([class_datetime == expect_datetime
                for class_datetime, expect_datetime in zip(my_event.alarms, alarms)])


def test_start_stop_ringing():

    # First day
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=20, second=0)
    is_alarm, events = myCalendar.is_alarm_today(one_date, reset_hour=True)

    my_event.set_event(is_alarm, events)

    # Before event
    alarm_is_ringing = my_event.is_ringing(one_date)
    assert alarm_is_ringing is False
    assert my_event.active is True

    # At the time of the event
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=30, second=0)
    alarm_is_ringing = my_event.is_ringing(one_date)
    assert alarm_is_ringing is True
    assert my_event.active is True

    # Stop ringing
    my_event.stop_alarm()

    # New test at the same time
    alarm_is_ringing = my_event.is_ringing(one_date)
    assert alarm_is_ringing is False
    assert my_event.active is False


def test_end_of_datetime_range():

    # First day
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=20, second=0)
    is_alarm, events = myCalendar.is_alarm_today(one_date, reset_hour=True)

    my_event.set_event(is_alarm, events)

    # At the time of the event
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=30, second=0)
    alarm_is_ringing = my_event.is_ringing(one_date)
    assert alarm_is_ringing is True
    assert my_event.active is True

    # At the last minute of the event
    alarm_is_ringing = my_event.is_ringing(one_date + datetime.timedelta(hours=1))
    assert alarm_is_ringing is True
    assert my_event.active is True

    # After the end of
    alarm_is_ringing = my_event.is_ringing(one_date + datetime.timedelta(hours=1, minutes=1))
    assert alarm_is_ringing is False
    assert my_event.active is True


def test_snooze_ringing():
    # First day
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=20, second=0)
    is_alarm, events = myCalendar.is_alarm_today(one_date, reset_hour=True)

    my_event.set_event(is_alarm, events)

    # At the time of the event
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=30, second=0)
    alarm_is_ringing = my_event.is_ringing(one_date)
    assert alarm_is_ringing is True
    assert my_event.active is True

    # Stop ringing
    my_event.snooze()

    # New test at the same time
    alarm_is_ringing = my_event.is_ringing(one_date)
    assert alarm_is_ringing is False
    assert my_event.active is True
    assert len(my_event.alarms) == 5

    # 5 minutes later
    alarm_is_ringing = my_event.is_ringing(one_date + datetime.timedelta(minutes=5))
    assert alarm_is_ringing is False
    assert my_event.active is True

    # 10 minutes later
    alarm_is_ringing = my_event.is_ringing(one_date + datetime.timedelta(minutes=10))
    assert alarm_is_ringing is True
    assert my_event.active is True



