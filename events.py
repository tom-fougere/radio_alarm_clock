from datetime import datetime, timedelta
import re

import logging


logger = logging.getLogger("radioAlarmLogger")


class RadioEvent:
    def __init__(self):
        self.raw = None

        self.id = ''
        self.is_alarm = False
        self.title = ''
        self.start_time = datetime.min
        self.end_time = datetime.min
        self.alarms = []
        self.radio = 'nrj'
        self.repetition = 10

        self.active = True
        self.ringing = False

    def set_event(self, is_alarm, event):

        self.is_alarm = is_alarm
        self.raw = event

        self.format_data()
        self.set_alarm_repetition()

    def format_data(self):

        self.title = self.raw.title

        # Set the start/end time as datetime (Remove useless timezone)
        if self.raw.kind == 'Hour':
            self.start_time = datetime.strptime(self.raw.start, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
            self.end_time = datetime.strptime(self.raw.end, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
        else:
            self.start_time = datetime.strptime(self.raw.start, '%Y-%m-%d').replace(tzinfo=None)
            self.end_time = datetime.strptime(self.raw.end, '%Y-%m-%d').replace(tzinfo=None)

        # Set radio
        self.set_radio(extract_information_with_hashtag(self.raw.description, "#radio"))

        # Set repetition: Extract the digit of the repetition text
        text_repetition = extract_information_with_hashtag(self.raw.description, "#repetition")
        digits_pattern = "([0-9]{1,2})"
        digits_search = re.search(digits_pattern, text_repetition)
        if len(text_repetition) > 0 and digits_search:
            self.set_repetition(digits_search.group(1))
        else:
            logger.debug("There is no #repetition of no digits")

    def set_radio(self, radio_str):

        if len(radio_str) > 0:
            logger.info("Set radio from %s to %s", self.radio, radio_str)
            self.radio = radio_str

    def set_repetition(self, repetition_value):

        if len(repetition_value) > 0:
            logger.info("Set number of repetition from %s to %s", self.repetition, repetition_value)
            self.repetition = int(repetition_value)

    def is_ringing(self, current_datetime):
        if self.start_time <= current_datetime <= self.end_time:
            if self.active is True:
                if self.ringing is False:
                    if current_datetime.replace(second=0, microsecond=0) in self.alarms:
                        self.ringing = True
                        self.alarms.pop(0)  # Remove first alarm to avoid new alarm for the same datetime
                        logger.info("Alarm must ring now")
                    else:
                        self.ringing = False
            else:
                self.ringing = False
        else:
            self.ringing = False

        return self.ringing

    def snooze(self):
        logger.info('Snooze !')
        self.ringing = False

    def stop_alarm(self):
        logger.info('Stop Alarm !')
        self.active = False

    def set_alarm_repetition(self):

        if self.is_alarm is True:
            self.alarms = []  # Reset alarms

            repet_datetime = self.start_time
            while repet_datetime < self.end_time:
                self.alarms.append(repet_datetime)
                repet_datetime += timedelta(minutes=self.repetition)

    def clear_event(self):
        logger.debug("Clear event")
        self.raw = None

        self.id = ''
        self.is_alarm = False
        self.title = ''
        self.start_time = datetime.min
        self.end_time = datetime.min
        self.alarms = []
        self.radio = 'nrj'
        self.repetition = 10

        self.active = True
        self.ringing = False


class CalendarEvent:
    def __init__(self, calendar_item, calendar_name, name):

        self.calendar_name = calendar_name
        self.name = name

        if len(calendar_item) == 0:
            self.kind = 'None'  # 'None', 'Hour', 'Day'
            self.is_alarm = False
        else:
            self.id = get_value_from_dict(calendar_item, 'id')
            self.title = get_value_from_dict(calendar_item, 'summary', '')
            self.description = get_value_from_dict(calendar_item, 'description', '')

            if 'dateTime' in calendar_item['start']:
                self.kind = 'Hour'
                self.start = calendar_item['start']['dateTime']
                self.end = calendar_item['end']['dateTime']
            elif 'date' in calendar_item['start']:
                self.kind = 'Day'
                self.start = calendar_item['start']['date']
                self.end = calendar_item['end']['date']

    def __eq__(self, other):
        if isinstance(other, CalendarEvent):
            return self.calendar_name == other.calendar_name and\
                   self.kind == other.kind and\
                   self.name == other.name and\
                   self.id == other.id and\
                   self.title == other.title and\
                   self.description == other.description and\
                   self.start == other.start and\
                   self.end == other.end
        return False


def convert_google_events_to_calendar_events(google_events, name):
    """
    Convert google events into calendar events
    :param google_events: google events, format of google calendar API event
    :param name: Chosen name for the calendarS, String
    :return:
        - list_events: List of calendarEvent
    """

    list_events = []
    for current_event in google_events['items']:
        my_calendar_event = CalendarEvent(current_event, google_events['summary'], name=name)
        list_events.append(my_calendar_event)

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


def extract_information_with_hashtag(full_text, hashtag):
    """
    Extract text after a defined hashtag
    :param full_text: Text with hashtag and needed information, string
    :param hashtag: Hashtag to search, string, example: #radio
    :return:
        - information: Information after a hashtag
    """

    # Add # at the end
    full_text = ''.join([full_text, '#'])

    # Search hashtag key
    index_defined_hashtag = full_text.find(hashtag)
    index_next_hashtag = full_text.find('#', index_defined_hashtag + 1)

    # Extract information and remove '\n' character
    information = full_text[index_defined_hashtag + len(hashtag) + 1: index_next_hashtag]
    information = information.rstrip()

    return information
