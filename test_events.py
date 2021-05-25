from events import *
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
    is_alarm, event = myCalendar.is_alarm_today(one_date)

    my_alarm.set_event(is_alarm, event)

    assert my_alarm.title == '#force essai1 - 9:30'
    assert my_alarm.is_alarm is True
    assert my_alarm.radio == 'nrj'  # default value
    assert my_alarm.repetition == 10  # default value
    assert my_alarm.event == event
    assert my_alarm.active == True
    assert my_alarm.ringing == False

    # Second day
    one_date = datetime.datetime(2020, 3, 31)
    is_alarm, event = myCalendar.is_alarm_today(one_date)

    my_alarm.set_event(is_alarm, event)

    assert my_alarm.title == 'essai2 - 12:00'
    assert my_alarm.is_alarm is True
    assert my_alarm.radio == 'nrj'  # default value
    assert my_alarm.repetition == 10  # default value
    assert my_alarm.event == event
    assert my_alarm.active == True
    assert my_alarm.ringing == False

    # Third day
    one_date = datetime.datetime(2020, 4, 1)
    is_alarm, event = myCalendar.is_alarm_today(one_date)

    my_alarm.set_event(is_alarm, event)

    assert my_alarm.title == 'essai3 - 15:30'
    assert my_alarm.is_alarm is True
    assert my_alarm.radio == 'fun'
    assert my_alarm.repetition == 15
    assert my_alarm.event == event
    assert my_alarm.active == True
    assert my_alarm.ringing == False


def test_set_no_event():

    # One day
    one_date = datetime.datetime(2020, 3, 24)
    is_alarm, event = myCalendar.is_alarm_today(one_date)

    my_alarm.set_event(is_alarm, event)

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
    is_alarm, event = myCalendar.is_alarm_today(one_date)

    my_alarm.set_event(is_alarm, event)

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
    is_alarm, event = myCalendar.is_alarm_today(one_date, reset_hour=True)

    my_alarm.set_event(is_alarm, event)

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
    is_alarm, event = myCalendar.is_alarm_today(one_date, reset_hour=True)

    my_alarm.set_event(is_alarm, event)

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
    is_alarm, event = myCalendar.is_alarm_today(one_date, reset_hour=True)

    my_alarm.set_event(is_alarm, event)

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

#################################################
# Tests on Event
#################################################
def test_no_event():

    google_event_dict = dict()

    # No event
    calendar_event = Event(google_event_dict, calendar_name='test', name='name')

    assert calendar_event.kind == 'None'
    assert calendar_event.calendar_name == 'test'
    assert calendar_event.name == 'name'
    assert calendar_event.title == ''

    count_field = 0
    for field in ['start', 'end', 'description', 'id']:
        if hasattr(calendar_event, field):
            count_field += 1
    assert count_field == 0

def test_event_hour():

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['description'] = 'my description'
    google_event_dict['start'] = dict()
    google_event_dict['start']['dateTime'] = '2021-05-25T10:51:00+0000'
    google_event_dict['end'] = dict()
    google_event_dict['end']['dateTime'] = '2021-05-25T11:51:00+0000'

    calendar_event = Event(google_event_dict, 'test', name='name')

    assert calendar_event.kind == 'Hour'
    assert calendar_event.calendar_name == 'test'
    assert calendar_event.name == 'name'
    assert calendar_event.title == 'my summary'
    assert calendar_event.description == 'my description'
    assert calendar_event.start == datetime.datetime(2021, 5, 25, 10, 51, 0)
    assert calendar_event.end == datetime.datetime(2021, 5, 25, 11, 51, 0)

    count_field = 0
    for field in ['start', 'end', 'title', 'description', 'id']:
        if hasattr(calendar_event, field):
            count_field += 1
    assert count_field == 5

def test_event_fullday():

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['start'] = dict()
    google_event_dict['start']['date'] = '2021-05-25'
    google_event_dict['end'] = dict()
    google_event_dict['end']['date'] = '2021-05-26'

    calendar_event = Event(google_event_dict, 'test', name='name')

    assert calendar_event.kind == 'Day'
    assert calendar_event.calendar_name == 'test'
    assert calendar_event.name == 'name'

    count_field = 0
    for field in ['start', 'end', 'title', 'description', 'id']:
        if hasattr(calendar_event, field):
            count_field += 1
    assert count_field == 5

def test_event_is_same():

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['start'] = dict()
    google_event_dict['start']['date'] = '2021-05-25'
    google_event_dict['end'] = dict()
    google_event_dict['end']['date'] = '2021-05-26'

    calendar_event1 = Event(google_event_dict, 'test', name='name')
    calendar_event2 = Event(google_event_dict, 'test', name='name')

    assert calendar_event1 == calendar_event2

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['start'] = dict()
    google_event_dict['start']['date'] = '2021-05-25'
    google_event_dict['end'] = dict()
    google_event_dict['end']['date'] = '2021-05-25'

    calendar_event3 = Event(google_event_dict, 'test', name='name')

    assert calendar_event2 != calendar_event3


def test_event_set_params():

    google_event_dict = dict()

    # No event
    calendar_event = Event(google_event_dict, calendar_name='test', name='name')

    assert calendar_event.kind == 'None'
    assert calendar_event.calendar_name == 'test'
    assert calendar_event.name == 'name'
    assert calendar_event.title == ''

    count_field = 0
    for field in ['start', 'end', 'description', 'id']:
        if hasattr(calendar_event, field):
            count_field += 1
    assert count_field == 0

    # Set params
    parameters = dict()
    parameters['name'] = 'new name'
    parameters['title'] = 'new title'
    parameters['start'] = 'new start'
    parameters['id'] = 'new id'
    calendar_event.set_params(parameters)

    count_field = 0
    for field in ['start', 'end', 'description', 'id']:
        if hasattr(calendar_event, field):
            count_field += 1
    assert count_field == 2

    assert calendar_event.name == "new name"
    assert calendar_event.title == "new title"
    assert calendar_event.start == "new start"
    assert calendar_event.id == "new id"


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
    assert calendar_events[0].start == datetime.datetime(2020, 4, 3, 10, 00, 00)
    assert calendar_events[0].end == datetime.datetime(2020, 4, 3, 10,30, 0)
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
    assert calendar_events[0].start == datetime.datetime(2020, 4, 3, 10, 00, 00)
    assert calendar_events[0].end == datetime.datetime(2020, 4, 3, 10,30, 0)
    assert calendar_events[0].id == '6kfnrm8phlcil6sha9t07rr3uh'
    assert calendar_events[0].name == 'name'
    assert calendar_events[0].kind == 'Hour'


def test_convert_google_events_to_calendar_events_no_event():
    one_date = datetime.datetime(2020, 4, 5, hour=9, minute=20, second=0)

    google_service = GoogleCalendarAPI()
    google_service.init_calendar_service()
    google_events = google_service.get_events_from_day(my_calendars['Reveil'], one_date)

    calendar_events = convert_google_events_to_calendar_events(google_events, name='name')

    assert len(calendar_events) == 1

    assert calendar_events[0].calendar_name == 'Réveil'
    assert calendar_events[0].name == 'name'
    assert calendar_events[0].kind == 'None'
    assert calendar_events[0].title == ''


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

