from alarms import *
from AlarmCalendar import *
from documents.rw_dict import *

myCalendar = OnlineCalendar()    # Init state
my_calendars = read_dict_file('documents/my_calendars.txt')
myCalendar.set_calendars(alarm_calendar=my_calendars['Reveil'],
                         public_holiday_calendar=my_calendars['Jours Feries'],
                         personal_calendar=my_calendars['Elise et Tom'])

my_alarm = Alarm()


def setup_function():
    my_alarm.clear_event()

#################################################
# Tests on RadioEvent
#################################################
def test_default_value():

    assert my_alarm.title == ''
    assert my_alarm.is_alarm is False
    assert my_alarm.radio == 'nrj'  # default value
    assert my_alarm.repetition == 10  # default value
    assert my_alarm.alarms_repetition == []  # default value
    assert my_alarm.event.kind == 'None'
    assert my_alarm.active == True
    assert my_alarm.ringing == False


def test_set_event():

    # First day
    one_date = datetime.datetime(2020, 3, 30)
    events = myCalendar.get_events(one_date)

    my_alarm.set_event(events[0])

    assert my_alarm.title == '#force essai1 - 9:30'
    assert my_alarm.is_alarm is True
    assert my_alarm.radio == 'nrj'  # default value
    assert my_alarm.repetition == 10  # default value
    assert my_alarm.event == events[0]
    assert my_alarm.active == True
    assert my_alarm.ringing == False

    # Second day
    one_date = datetime.datetime(2020, 3, 31)
    events = myCalendar.get_events(one_date)

    my_alarm.set_event(events[0])

    assert my_alarm.title == 'essai2 - 12:00'
    assert my_alarm.is_alarm is True
    assert my_alarm.radio == 'nrj'  # default value
    assert my_alarm.repetition == 10  # default value
    assert my_alarm.event == events[0]
    assert my_alarm.active == True
    assert my_alarm.ringing == False

    # Third day
    one_date = datetime.datetime(2020, 4, 1)
    events = myCalendar.get_events(one_date)

    my_alarm.set_event(events[0])

    assert my_alarm.title == 'essai3 - 15:30'
    assert my_alarm.is_alarm is True
    assert my_alarm.radio == 'fun'
    assert my_alarm.repetition == 15
    assert my_alarm.event == events[0]
    assert my_alarm.active == True
    assert my_alarm.ringing == False


def test_set_no_event():

    # One day
    one_date = datetime.datetime(2020, 3, 24)
    events = myCalendar.get_events(one_date)

    my_alarm.set_event(events[0])

    assert my_alarm.title == ''
    assert my_alarm.is_alarm is False
    assert my_alarm.radio == 'nrj'
    assert my_alarm.repetition == 10
    assert my_alarm.event.kind == 'None'
    assert my_alarm.active == True
    assert my_alarm.ringing == False


def test_list_of_alarms():

    # First day
    one_date = datetime.datetime(2020, 3, 30)
    events = myCalendar.get_events(one_date)

    my_alarm.set_event(events[0])

    alarms = [datetime.datetime(2020, 3, 30, hour=9, minute=30),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=10),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=20),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=30),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=40),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=50)]

    assert len(my_alarm.alarms_repetition) == 6
    assert all([class_datetime == expect_datetime
                for class_datetime, expect_datetime in zip(my_alarm.alarms_repetition, alarms)])


def test_start_stop_ringing():

    # First day
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=20, second=0)
    events = myCalendar.get_events(one_date, reset_hour=True)

    my_alarm.set_event(events[0])

    # Before event
    alarm_is_ringing = my_alarm.is_ringing(one_date)
    assert alarm_is_ringing is False
    assert my_alarm.active is True

    # At the time of the event
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=30, second=0)
    alarm_is_ringing = my_alarm.is_ringing(one_date)
    assert alarm_is_ringing is True
    assert my_alarm.active is True

    # Stop ringing
    my_alarm.stop_alarm()

    # New test at the same time
    alarm_is_ringing = my_alarm.is_ringing(one_date)
    assert alarm_is_ringing is False
    assert my_alarm.active is False


def test_end_of_datetime_range():

    # First day
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=20, second=0)
    events = myCalendar.get_events(one_date, reset_hour=True)

    my_alarm.set_event(events[0])

    # At the time of the event
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=30, second=0)
    alarm_is_ringing = my_alarm.is_ringing(one_date)
    assert alarm_is_ringing is True
    assert my_alarm.active is True

    # At the last minute of the event
    alarm_is_ringing = my_alarm.is_ringing(one_date + datetime.timedelta(hours=1))
    assert alarm_is_ringing is True
    assert my_alarm.active is True

    # After the end of
    alarm_is_ringing = my_alarm.is_ringing(one_date + datetime.timedelta(hours=1, minutes=1))
    assert alarm_is_ringing is False
    assert my_alarm.active is True


def test_snooze_ringing():
    # First day
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=20, second=0)
    events = myCalendar.get_events(one_date, reset_hour=True)

    my_alarm.set_event(events[0])

    # At the time of the event
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=30, second=0)
    alarm_is_ringing = my_alarm.is_ringing(one_date)
    assert alarm_is_ringing is True
    assert my_alarm.active is True

    # Stop ringing
    my_alarm.snooze()

    # New test at the same time
    alarm_is_ringing = my_alarm.is_ringing(one_date)
    assert alarm_is_ringing is False
    assert my_alarm.active is True
    assert len(my_alarm.alarms_repetition) == 5

    # 5 minutes later
    alarm_is_ringing = my_alarm.is_ringing(one_date + datetime.timedelta(minutes=5))
    assert alarm_is_ringing is False
    assert my_alarm.active is True

    # 10 minutes later
    alarm_is_ringing = my_alarm.is_ringing(one_date + datetime.timedelta(minutes=10))
    assert alarm_is_ringing is True
    assert my_alarm.active is True


def test_clear_event():

    # First day
    one_date = datetime.datetime(2020, 3, 30)
    events = myCalendar.get_events(one_date)

    my_alarm.set_event(events[0])
    my_alarm.active = False
    my_alarm.ringing = True

    assert my_alarm.title == '#force essai1 - 9:30'
    assert my_alarm.is_alarm is True
    assert my_alarm.radio == 'nrj'  # default value
    assert my_alarm.repetition == 10  # default value
    assert my_alarm.event == events[0]

    my_alarm.clear_event()

    assert my_alarm.title == ''
    assert my_alarm.is_alarm is False
    assert my_alarm.radio == 'nrj'  # default value
    assert my_alarm.repetition == 10  # default value
    assert my_alarm.alarms_repetition == []  # default value
    assert my_alarm.event.kind == 'None'
    assert my_alarm.active == True
    assert my_alarm.ringing == False


def test_set_active():

    # First day
    one_date = datetime.datetime(2020, 3, 30)
    events = myCalendar.get_events(one_date)

    my_alarm.set_event(events[0])
    my_alarm.active = False
    my_alarm.ringing = True

    my_alarm.set_active()

    assert my_alarm.active == True

#################################################
# Tests on extract_information_with_hashtag
#################################################

def test_extract_information_with_hashtag():

    information = extract_information_with_hashtag('#force mon texte', '#force')
    assert information == "mon texte"

    information = extract_information_with_hashtag('#force mon texte', '#mon')
    assert information == ""

    information = extract_information_with_hashtag('#force mon #texte', '#force')
    assert information == "mon"

    information = extract_information_with_hashtag('#force mon #texte test1 2 3 bateau #chau 6min', '#texte')
    assert information == "test1 2 3 bateau"

    information = extract_information_with_hashtag('', '#force')
    assert information == ""