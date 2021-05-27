from datetime import datetime
from utils import get_value_from_dict

import logging


OFF_STRING = '#off'
FORCE_STRING = '#force'

logger = logging.getLogger("radioAlarmLogger")


class Event:
    def __init__(self, calendar_item, calendar_name, is_alarm=False):

        self.calendar_name = calendar_name
        self.is_alarm = is_alarm

        if len(calendar_item) == 0:
            self.kind = 'None'  # 'None', 'Hour', 'Day'
            self.title = ''
            self.is_alarm = False  # Force to False in case of no event
        else:
            self.id = get_value_from_dict(calendar_item, 'id')
            self.title = get_value_from_dict(calendar_item, 'summary', '')
            self.description = get_value_from_dict(calendar_item, 'description', '')

            if 'dateTime' in calendar_item['start']:
                self.kind = 'Hour'
                self.start = datetime.strptime(calendar_item['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
                self.end = datetime.strptime(calendar_item['end']['dateTime'], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
            elif 'date' in calendar_item['start']:
                self.kind = 'Day'
                self.start = datetime.strptime(calendar_item['start']['date'], '%Y-%m-%d').replace(tzinfo=None)
                self.end = datetime.strptime(calendar_item['end']['date'], '%Y-%m-%d').replace(tzinfo=None)

    def __eq__(self, other):
        if isinstance(other, Event):
            return self.calendar_name == other.calendar_name and\
                   self.is_alarm == other.is_alarm and\
                   self.kind == other.kind and\
                   self.title == other.title and\
                   self.description == other.description and\
                   self.start == other.start and\
                   self.end == other.end and\
                   self.id == other.id
        return False

    def set_params(self, parameters):

        attributes = ['calendar_name', 'is_alarm', 'kind', 'title', 'id', 'description', 'start', 'end']
        for attr in attributes:
            if attr in parameters:
                setattr(self, attr, parameters[attr])


def convert_google_events_to_calendar_events(google_events, is_alarm=False):
    """
    Convert google events into calendar events
    :param google_events: google events, format of google calendar API event
    :param is_alarm: is the current an alarm ? String
    :return:
        - list_events: List of Event(s)
    """

    list_events = []
    for current_event in google_events['items']:
        my_calendar_event = Event(current_event, google_events['summary'], is_alarm=is_alarm)
        list_events.append(my_calendar_event)

    # Add a No-Event to the list in case of no event
    if len(google_events['items'])  == 0:
        list_events.append(Event([], google_events['summary'], is_alarm=False))

    return list_events



def sort_events(events_alarm_calendar, events_public_holiday_calendar, events_personal_calendar):
    """
    Sort events from 3 google calendars (alarm, public holiday and personal)
    order: #force, #off, public holiday, alarm, personal
    :param events_alarm_calendar: List of Events from the alarm calendar, Google service "Event"
    :param events_public_holiday_calendar: List of Events from the public holiday calendar, Google service "Event"
    :param events_personal_calendar: List of Events from the personal calendar, Google service "Event"
    :return:
        - list of sorted CalendarEvent
    """

    events_alarm = convert_google_events_to_calendar_events(events_alarm_calendar, is_alarm=True)
    events_public_holiday = convert_google_events_to_calendar_events(events_public_holiday_calendar, is_alarm=False)
    events_personal = convert_google_events_to_calendar_events(events_personal_calendar, is_alarm=False)

    full_list = events_public_holiday + events_alarm + events_personal
    sorted_events = []

    priority = 0
    index = 0
    while len(full_list) > 0:
        event = full_list[index]

        if priority == 0:
            if event.title.lower().find(FORCE_STRING)>=0:  # FORCE
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        elif priority == 1:
            if event.title.lower().find(OFF_STRING) >= 0:  # OFF
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        elif priority == 2:
            if event.kind != 'None' and event.is_alarm == True:
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        elif priority == 3:
            if event.kind != 'None' and event.is_alarm == False:
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        elif priority == 4:
            sorted_events.append(event)
            full_list.pop(index)

        if index >= len(full_list):
            priority +=1
            index = 0

    return sorted_events
