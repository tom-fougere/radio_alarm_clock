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
    myCalendar.init_calendar_service()
    events = myCalendar.get_events_from_day('primary', '2021', '03', '24')

    assert len(events['items']) == 2

    event_available = False
    for event in events['items']:
        if event['summary'] == 'Test calendarAPI':
            event_available = True

    assert event_available is True

    events = myCalendar.get_events_from_day('primary', '2021', '03', '24', '10', '01')
    assert len(events['items']) == 1

