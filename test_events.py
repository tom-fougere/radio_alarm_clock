from events import *
from AlarmCalendar import *
from documents.rw_dict import *

myCalendar = OnlineCalendar()    # Init state
my_calendars = read_dict_file('documents/my_calendars.txt')
myCalendar.set_calendars(alarm_calendar=my_calendars['Reveil'],
                         public_holiday_calendar=my_calendars['Jours Feries'],
                         personal_calendar=my_calendars['Elise et Tom'])

#################################################
# Tests on Event
#################################################
def test_no_event():

    google_event_dict = dict()

    # No event
    calendar_event = Event(google_event_dict, calendar_name='test', is_alarm=True)

    assert calendar_event.kind == 'None'
    assert calendar_event.calendar_name == 'test'
    assert calendar_event.is_alarm == False
    assert calendar_event.title == ''
    assert calendar_event.description == ''
    assert calendar_event.start == datetime.datetime.min
    assert calendar_event.end == datetime.datetime.min

def test_event_hour():

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['description'] = 'my description'
    google_event_dict['start'] = dict()
    google_event_dict['start']['dateTime'] = '2021-05-25T10:51:00+0000'
    google_event_dict['end'] = dict()
    google_event_dict['end']['dateTime'] = '2021-05-25T11:51:00+0000'

    calendar_event = Event(google_event_dict, 'test', is_alarm=True)

    assert calendar_event.kind == 'Hour'
    assert calendar_event.calendar_name == 'test'
    assert calendar_event.is_alarm == True
    assert calendar_event.title == 'my summary'
    assert calendar_event.description == 'my description'
    assert calendar_event.start == datetime.datetime(2021, 5, 25, 10, 51, 0)
    assert calendar_event.end == datetime.datetime(2021, 5, 25, 11, 51, 0)


def test_event_fullday():

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['start'] = dict()
    google_event_dict['start']['date'] = '2021-05-25'
    google_event_dict['end'] = dict()
    google_event_dict['end']['date'] = '2021-05-26'

    calendar_event = Event(google_event_dict, 'test',  is_alarm=True)

    assert calendar_event.kind == 'Day'
    assert calendar_event.calendar_name == 'test'
    assert calendar_event.is_alarm == True

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

    calendar_event1 = Event(google_event_dict, 'test', is_alarm=True)
    calendar_event2 = Event(google_event_dict, 'test', is_alarm=True)

    assert calendar_event1 == calendar_event2

    google_event_dict = dict()
    google_event_dict['id'] = '0123456789'
    google_event_dict['summary'] = 'my summary'
    google_event_dict['start'] = dict()
    google_event_dict['start']['date'] = '2021-05-25'
    google_event_dict['end'] = dict()
    google_event_dict['end']['date'] = '2021-05-25'

    calendar_event3 = Event(google_event_dict, 'test', is_alarm=True)

    assert calendar_event2 != calendar_event3


def test_event_set_params():

    google_event_dict = dict()

    # No event
    calendar_event = Event(google_event_dict, calendar_name='test', is_alarm=False)

    assert calendar_event.kind == 'None'
    assert calendar_event.calendar_name == 'test'
    assert calendar_event.is_alarm == False
    assert calendar_event.title == ''

    # Set params
    parameters = dict()
    parameters['title'] = 'new title'
    parameters['calendar_name'] = 'new calendar name'
    parameters['description'] = 'new description'
    parameters['start'] = 'new start'
    parameters['end'] = 'new end'
    parameters['id'] = 'new id'
    parameters['is_alarm'] = True
    parameters['no_attribute'] = 'no_attribute'

    calendar_event.set_params(parameters)

    assert calendar_event.kind == 'None'
    assert calendar_event.calendar_name == 'new calendar name'
    assert calendar_event.is_alarm == True
    assert calendar_event.title == 'new title'
    assert calendar_event.description == 'new description'
    assert calendar_event.start == 'new start'
    assert calendar_event.end == 'new end'
    assert calendar_event.id == "new id"

    assert hasattr(calendar_event, 'no_attribute') is False


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

    calendar_events = convert_google_events_to_calendar_events(google_events, is_alarm=False)

    assert calendar_events[0].calendar_name == 'Réveil'
    assert calendar_events[0].title == 'Reveil 4'
    assert calendar_events[0].description == '#radio nrj\n#repetition 5'
    assert calendar_events[0].start == datetime.datetime(2020, 4, 3, 10, 00, 00)
    assert calendar_events[0].end == datetime.datetime(2020, 4, 3, 10, 30, 0)
    assert calendar_events[0].id == '6kfnrm8phlcil6sha9t07rr3uh'
    assert calendar_events[0].is_alarm == False
    assert calendar_events[0].kind == 'Hour'

def test_convert_google_events_to_calendar_events_is_alarm():

    one_date = datetime.datetime(2020, 4, 3, hour=9, minute=20, second=0)

    google_service = GoogleCalendarAPI()
    google_service.init_calendar_service()
    google_events = google_service.get_events_from_day(my_calendars['Reveil'], one_date)

    calendar_events = convert_google_events_to_calendar_events(google_events, is_alarm=True)

    assert calendar_events[0].calendar_name == 'Réveil'
    assert calendar_events[0].title == 'Reveil 4'
    assert calendar_events[0].description == '#radio nrj\n#repetition 5'
    assert calendar_events[0].start == datetime.datetime(2020, 4, 3, 10, 00, 00)
    assert calendar_events[0].end == datetime.datetime(2020, 4, 3, 10,30, 0)
    assert calendar_events[0].id == '6kfnrm8phlcil6sha9t07rr3uh'
    assert calendar_events[0].is_alarm == True
    assert calendar_events[0].kind == 'Hour'


def test_convert_google_events_to_calendar_events_no_event():
    one_date = datetime.datetime(2020, 4, 5, hour=9, minute=20, second=0)

    google_service = GoogleCalendarAPI()
    google_service.init_calendar_service()
    google_events = google_service.get_events_from_day(my_calendars['Reveil'], one_date)

    calendar_events = convert_google_events_to_calendar_events(google_events, is_alarm=True)

    assert len(calendar_events) == 1

    assert calendar_events[0].calendar_name == 'Réveil'
    assert calendar_events[0].is_alarm == False
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

    assert sorted_events[0].is_alarm == True
    assert sorted_events[1].is_alarm == False
    assert sorted_events[2].is_alarm == True
    assert sorted_events[3].is_alarm == False

