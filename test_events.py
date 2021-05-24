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
    calendar_event = CalendarEvent(google_event_dict, calendar_name='test', name='name')

    assert calendar_event.kind == 'None'
    assert calendar_event.calendar_name == 'test'
    assert calendar_event.name == 'name'

    count_field = 0
    for field in ['start', 'end', 'title', 'description', 'id']:
        if hasattr(calendar_event, field):
            count_field += 1
    assert count_field == 0

def test_calendar_event_hour():

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['description'] = 'my description'
    google_event_dict['start'] = dict()
    google_event_dict['start']['dateTime'] = 'my start'
    google_event_dict['end'] = dict()
    google_event_dict['end']['dateTime'] = 'my end'

    calendar_event = CalendarEvent(google_event_dict, 'test', name='name')

    assert calendar_event.kind == 'Hour'
    assert calendar_event.calendar_name == 'test'
    assert calendar_event.name == 'name'
    assert calendar_event.title == 'my summary'
    assert calendar_event.description == 'my description'
    assert calendar_event.start == 'my start'
    assert calendar_event.end == 'my end'

    count_field = 0
    for field in ['start', 'end', 'title', 'description', 'id']:
        if hasattr(calendar_event, field):
            count_field += 1
    assert count_field == 5

def test_calendar_event_fullday():

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['start'] = dict()
    google_event_dict['start']['date'] = 'my start'
    google_event_dict['end'] = dict()
    google_event_dict['end']['date'] = 'my end'

    calendar_event = CalendarEvent(google_event_dict, 'test', name='name')

    assert calendar_event.kind == 'Day'
    assert calendar_event.calendar_name == 'test'
    assert calendar_event.name == 'name'

    count_field = 0
    for field in ['start', 'end', 'title', 'description', 'id']:
        if hasattr(calendar_event, field):
            count_field += 1
    assert count_field == 5

def test_calendar_event_is_same():

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['start'] = dict()
    google_event_dict['start']['date'] = 'my start'
    google_event_dict['end'] = dict()
    google_event_dict['end']['date'] = 'my end'

    calendar_event1 = CalendarEvent(google_event_dict, 'test', name='name')
    calendar_event2 = CalendarEvent(google_event_dict, 'test', name='name')

    assert calendar_event1 == calendar_event2

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['start'] = dict()
    google_event_dict['start']['date'] = 'my new start'
    google_event_dict['end'] = dict()
    google_event_dict['end']['date'] = 'my end'

    calendar_event3 = CalendarEvent(google_event_dict, 'test', name='name')

    assert calendar_event2 != calendar_event3


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

    one_date = datetime.datetime(2020, 4, 3, hour=9, minute=20, second=0)

    google_service = GoogleCalendarAPI()
    google_service.init_calendar_service()
    google_events = google_service.get_events_from_day(my_calendars['Reveil'], one_date)

    calendar_events = convert_google_events_to_calendar_events(google_events, name='name')

    assert calendar_events[0].calendar_name == 'Réveil'
    assert calendar_events[0].title == 'Reveil 4'
    assert calendar_events[0].description == '#radio nrj\n#repetition 5'
    assert calendar_events[0].start == '2020-04-03T10:00:00+02:00'
    assert calendar_events[0].end == '2020-04-03T10:30:00+02:00'
    assert calendar_events[0].id == '6kfnrm8phlcil6sha9t07rr3uh'
    assert calendar_events[0].name == 'name'
    assert calendar_events[0].kind == 'Hour'

def test_convert_google_events_to_calendar_events_is_alarm():

    one_date = datetime.datetime(2020, 4, 3, hour=9, minute=20, second=0)

    google_service = GoogleCalendarAPI()
    google_service.init_calendar_service()
    google_events = google_service.get_events_from_day(my_calendars['Reveil'], one_date)

    calendar_events = convert_google_events_to_calendar_events(google_events, name='name')

    assert calendar_events[0].calendar_name == 'Réveil'
    assert calendar_events[0].title == 'Reveil 4'
    assert calendar_events[0].description == '#radio nrj\n#repetition 5'
    assert calendar_events[0].start == '2020-04-03T10:00:00+02:00'
    assert calendar_events[0].end == '2020-04-03T10:30:00+02:00'
    assert calendar_events[0].id == '6kfnrm8phlcil6sha9t07rr3uh'
    assert calendar_events[0].name == 'name'
    assert calendar_events[0].kind == 'Hour'


#################################################
# Tests on convert_google_events_to_calendar_events
#################################################
def test_sort_events():

    one_date = datetime.datetime(2020, 4, 4, hour=0, minute=20, second=0)

    google_service = GoogleCalendarAPI()
    google_service.init_calendar_service()
    google_events_alarm = google_service.get_events_from_day(my_calendars['Reveil'], one_date)
    google_events_public_holyday = google_service.get_events_from_day(my_calendars['Jours Feries'], one_date)
    google_events_personal = google_service.get_events_from_day(my_calendars['Elise et Tom'], one_date)

    sorted_events = sort_events(google_events_alarm, google_events_public_holyday, google_events_personal)

    assert sorted_events[0].name == 'Alarm'
    assert sorted_events[1].name == 'Personal'
    assert sorted_events[2].name == 'Alarm'
    assert sorted_events[3].name == 'Personal'

