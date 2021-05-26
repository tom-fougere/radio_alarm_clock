from calendarAPI import *
from documents.rw_dict import *

myCalendar = GoogleCalendarAPI()


def test_list_calendars():
    myCalendar.init_calendar_service()
    calendars_name = myCalendar.get_list_calendars_name()
    calendars_id = myCalendar.get_list_calendars_id()

    mandatory_calendars = read_dict_file('documents/mandatory_calendars.txt')

    count_name = 0
    count_id = 0
    for name, id in mandatory_calendars.items():
        if name in calendars_name:
            count_name += 1
        if id in calendars_id:
            count_id += 1

    assert count_name == len(mandatory_calendars)
    assert count_id == len(mandatory_calendars)


def test_events_in_calendar():
    one_date = datetime.datetime(2021, 3, 24)
    myCalendar.init_calendar_service()
    events = myCalendar.get_events_from_day('primary', one_date)

    assert len(events['items']) == 2

    event_available = False
    for event in events['items']:
        if event['summary'] == 'Test calendarAPI':
            event_available = True

    assert event_available is True

    # Search events after a defined time
    one_date = datetime.datetime(2021, 3, 24, hour=14, minute=1)
    events = myCalendar.get_events_from_day('primary', one_date)
    assert len(events['items']) == 1

    # Reset hour to 0:00:00
    events = myCalendar.get_events_from_day('primary', one_date, reset_hour=True)
    assert len(events['items']) == 2


def test_add_delete_event():

    my_calendars = read_dict_file('documents/my_calendars.txt')

    myCalendar.init_calendar_service()

    event = {
        'summary': 'Test Event',
        'description': 'An event added with UT in test_calendarAPI.py',
        'start': {
            'dateTime': '2020-03-28T09:00:00',
            'timeZone': 'Europe/Paris',
        },
        'end': {
            'dateTime': '2020-03-28T17:00:00',
            'timeZone': 'Europe/Paris',
        },
    }

    list_events = myCalendar.get_events_from_day(my_calendars['Reveil'], datetime.datetime(2020, 3, 28))
    assert len(list_events['items']) == 0

    inserted_event = myCalendar.add_event(event, calendar_id=my_calendars['Reveil'])

    list_events = myCalendar.get_events_from_day(my_calendars['Reveil'], datetime.datetime(2020, 3, 28))
    assert len(list_events['items']) == 1
    assert inserted_event == list_events['items'][0]

    myCalendar.delete_event(inserted_event, calendar_id=my_calendars['Reveil'])


