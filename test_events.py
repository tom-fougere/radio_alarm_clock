from events import *
from AlarmCalendar import *
from documents.rw_dict import *

myCalendar = AlarmCalendar()    # Init state
my_calendars = read_dict_file('documents/my_calendars.txt')
myCalendar.set_calendars(alarm_calendar=my_calendars['Reveil'],
                         public_holiday_calendar=my_calendars['Jours Feries'],
                         personal_calendar=my_calendars['Elise et Tom'])

my_radio_event = RadioEvent()


def setup_function():
    my_radio_event.clear_event()

#################################################
# Tests on RadioEvent
#################################################
def test_set_radio_events():

    # First day
    one_date = datetime.datetime(2020, 3, 30)
    is_alarm, events = myCalendar.is_alarm_today(one_date)

    my_radio_event.set_event(is_alarm, events)

    assert my_radio_event.is_alarm is True
    assert my_radio_event.title == 'essai1'
    assert my_radio_event.start_time == datetime.datetime(2020, 3, 30, hour=9, minute=30)
    assert my_radio_event.end_time == datetime.datetime(2020, 3, 30, hour=10, minute=30)
    assert my_radio_event.radio == 'nrj'  # default value
    assert my_radio_event.repetition == 10  # default value

    # Second day
    one_date = datetime.datetime(2020, 3, 31)
    is_alarm, events = myCalendar.is_alarm_today(one_date)

    my_radio_event.set_event(is_alarm, events)

    assert my_radio_event.is_alarm is True
    assert my_radio_event.title == 'essai2'
    assert my_radio_event.start_time == datetime.datetime(2020, 3, 31, hour=12, minute=00)
    assert my_radio_event.end_time == datetime.datetime(2020, 3, 31, hour=13, minute=00)
    assert my_radio_event.radio == 'nrj'  # default value
    assert my_radio_event.repetition == 10  # default value

    # Third day
    one_date = datetime.datetime(2020, 4, 1)
    is_alarm, events = myCalendar.is_alarm_today(one_date)

    my_radio_event.set_event(is_alarm, events)

    assert my_radio_event.is_alarm is True
    assert my_radio_event.title == 'essai3'
    assert my_radio_event.start_time == datetime.datetime(2020, 4, 1, hour=15, minute=30)
    assert my_radio_event.end_time == datetime.datetime(2020, 4, 1, hour=16, minute=30)
    assert my_radio_event.radio == 'fun'
    assert my_radio_event.repetition == 15


def test_list_of_alarms():

    # First day
    one_date = datetime.datetime(2020, 3, 30)
    is_alarm, events = myCalendar.is_alarm_today(one_date)

    my_radio_event.set_event(is_alarm, events)

    alarms = [datetime.datetime(2020, 3, 30, hour=9, minute=30),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=10),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=20),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=30),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=40),
              datetime.datetime(2020, 3, 30, hour=9, minute=30) + datetime.timedelta(minutes=50)]

    assert len(my_radio_event.alarms) == 6
    assert all([class_datetime == expect_datetime
                for class_datetime, expect_datetime in zip(my_radio_event.alarms, alarms)])


def test_start_stop_ringing():

    # First day
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=20, second=0)
    is_alarm, events = myCalendar.is_alarm_today(one_date, reset_hour=True)

    my_radio_event.set_event(is_alarm, events)

    # Before event
    alarm_is_ringing = my_radio_event.is_ringing(one_date)
    assert alarm_is_ringing is False
    assert my_radio_event.active is True

    # At the time of the event
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=30, second=0)
    alarm_is_ringing = my_radio_event.is_ringing(one_date)
    assert alarm_is_ringing is True
    assert my_radio_event.active is True

    # Stop ringing
    my_radio_event.stop_alarm()

    # New test at the same time
    alarm_is_ringing = my_radio_event.is_ringing(one_date)
    assert alarm_is_ringing is False
    assert my_radio_event.active is False


def test_end_of_datetime_range():

    # First day
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=20, second=0)
    is_alarm, events = myCalendar.is_alarm_today(one_date, reset_hour=True)

    my_radio_event.set_event(is_alarm, events)

    # At the time of the event
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=30, second=0)
    alarm_is_ringing = my_radio_event.is_ringing(one_date)
    assert alarm_is_ringing is True
    assert my_radio_event.active is True

    # At the last minute of the event
    alarm_is_ringing = my_radio_event.is_ringing(one_date + datetime.timedelta(hours=1))
    assert alarm_is_ringing is True
    assert my_radio_event.active is True

    # After the end of
    alarm_is_ringing = my_radio_event.is_ringing(one_date + datetime.timedelta(hours=1, minutes=1))
    assert alarm_is_ringing is False
    assert my_radio_event.active is True


def test_snooze_ringing():
    # First day
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=20, second=0)
    is_alarm, events = myCalendar.is_alarm_today(one_date, reset_hour=True)

    my_radio_event.set_event(is_alarm, events)

    # At the time of the event
    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=30, second=0)
    alarm_is_ringing = my_radio_event.is_ringing(one_date)
    assert alarm_is_ringing is True
    assert my_radio_event.active is True

    # Stop ringing
    my_radio_event.snooze()

    # New test at the same time
    alarm_is_ringing = my_radio_event.is_ringing(one_date)
    assert alarm_is_ringing is False
    assert my_radio_event.active is True
    assert len(my_radio_event.alarms) == 5

    # 5 minutes later
    alarm_is_ringing = my_radio_event.is_ringing(one_date + datetime.timedelta(minutes=5))
    assert alarm_is_ringing is False
    assert my_radio_event.active is True

    # 10 minutes later
    alarm_is_ringing = my_radio_event.is_ringing(one_date + datetime.timedelta(minutes=10))
    assert alarm_is_ringing is True
    assert my_radio_event.active is True

#################################################
# Tests on CalendarEvent
#################################################
def test_no_calendar_event():

    google_event_dict = dict()

    # No event
    calendar_event = CalendarEvent(google_event_dict, 'test')

    assert calendar_event.kind == 'None'
    assert calendar_event.calendar_name == 'test'

    count_field = 0
    for field in ['start', 'end', 'description', 'id']:
        if hasattr(calendar_event, field):
            count_field += 1
    assert count_field == 0

def test_calendar_event_alarm():

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['start'] = dict()
    google_event_dict['start']['datetime'] = 'my start'
    google_event_dict['end'] = dict()
    google_event_dict['end']['datetime'] = 'my end'

    # No event
    calendar_event = CalendarEvent(google_event_dict, 'test')

    assert calendar_event.kind == 'Alarm'
    assert calendar_event.calendar_name == 'test'

    count_field = 0
    for field in ['start', 'end', 'description', 'id']:
        if hasattr(calendar_event, field):
            count_field += 1
    assert count_field == 4

def test_calendar_event_fullday():

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['start'] = dict()
    google_event_dict['start']['date'] = 'my start'
    google_event_dict['end'] = dict()
    google_event_dict['end']['date'] = 'my end'

    # No event
    calendar_event = CalendarEvent(google_event_dict, 'test')

    assert calendar_event.kind == 'FullDay'
    assert calendar_event.calendar_name == 'test'

    count_field = 0
    for field in ['start', 'end', 'description', 'id']:
        if hasattr(calendar_event, field):
            count_field += 1
    assert count_field == 4


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


#################################################
# Tests on get_value_from_dict
#################################################
def test_get_value_from_dict():

    my_dict = dict()
    my_dict['test'] = 123
    my_dict['field'] = 'string'
    my_dict[2] = 'test'

    value = get_value_from_dict(my_dict, 'test')
    assert value == 123

    value = get_value_from_dict(my_dict, 'field')
    assert value == 'string'

    value = get_value_from_dict(my_dict, 2)
    assert value == 'test'

    value = get_value_from_dict(my_dict, 'unknown')
    assert value == ''

    value = get_value_from_dict(my_dict, 'unknown', 'default')
    assert value == 'default'

#################################################
# Tests on convert_google_events_to_calendar_events
#################################################
def test_convert_google_events_to_calendar_events():

    one_date = datetime.datetime(2020, 3, 30, hour=9, minute=20, second=0)
    is_alarm, events = myCalendar.is_alarm_today(one_date, reset_hour=True)
    self.google_service.get_events_from_day(self.personal_calendar,
                                            today_datetime)

    calendar_events = convert_google_events_to_calendar_events(events)


