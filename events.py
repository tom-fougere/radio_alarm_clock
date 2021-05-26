from datetime import datetime

import logging


logger = logging.getLogger("radioAlarmLogger")


class Event:
    def __init__(self, calendar_item, calendar_name, name):

        self.calendar_name = calendar_name
        self.name = name

        if len(calendar_item) == 0:
            self.kind = 'None'  # 'None', 'Hour', 'Day'
            self.title = ''
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
                   self.name == other.name and\
                   self.kind == other.kind and\
                   self.title == other.title and\
                   self.description == other.description and\
                   self.start == other.start and\
                   self.end == other.end and\
                   self.id == other.id
        return False

    def set_params(self, parameters):

        attributes = ['calendar_name', 'name', 'kind', 'title', 'id', 'description', 'start', 'end']
        for attr in attributes:
            if attr in parameters:
                setattr(self, attr, parameters[attr])


def convert_google_events_to_calendar_events(google_events, name):
    """
    Convert google events into calendar events
    :param google_events: google events, format of google calendar API event
    :param name: Chosen name for the calendarS, String
    :return:
        - list_events: List of Event(s)
    """

    list_events = []
    for current_event in google_events['items']:
        my_calendar_event = Event(current_event, google_events['summary'], name=name)
        list_events.append(my_calendar_event)

    # Add a No-Event to the list in case of no event
    if len(google_events['items'])  == 0:
        list_events.append(Event([], google_events['summary'], name=name))

    return list_events


def get_value_from_dict(item_dict, wanted_field, default_value=''):
    """
    Get the value from a dictionary selecting the field. A default value is set if the field don't exist
    :param item_dict: dictionary to watch, dict
    :param wanted_field: field to search in the dictionary, string
    :param default_value: default value if the wanted field don't exist
    :return:
        - value: value of the dictionary with the wanted field
    """

    value = default_value
    if wanted_field in item_dict:
        value = item_dict[wanted_field]

    return value


def should_the_bell_be_turned_on(current_datetime, event_today, alarm_today, alarm_tomorrow, limit_hour=14):
    """
    In function of the context (datetime, today event and alarms), return flag for the bell display
    :param current_datetime: the current datetime (to compare with the limit_hour
    :param event_today: Event of the current datetime (today)
    :param alarm_today: Flag/Alarm of the current day
    :param alarm_tomorrow: Flag/Alarm of the next day
    :param limit_hour: Hour to switch between the alarm of the current day to the next day
    :return:
        - Flag for the bell displaying, boolean
    """

    if event_today.kind == 'Hour':
        if current_datetime <= event_today.end:
            display_bell_icon = alarm_today
        else:
            display_bell_icon = alarm_tomorrow
    else:
        if current_datetime < datetime(current_datetime.year, current_datetime.month, current_datetime.day,
                                       hour=limit_hour, minute=0, second=0):
            display_bell_icon = alarm_today
        else:
            display_bell_icon = alarm_tomorrow

    return display_bell_icon
