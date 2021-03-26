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

