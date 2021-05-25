from datetime import datetime, timedelta
import re

import logging


logger = logging.getLogger("radioAlarmLogger")


class Alarm:
    def __init__(self):
        self.event = Event([], 'no_calendar', 'no_name')

        self.title = ''
        self.is_alarm = False
        self.radio = 'nrj'
        self.repetition = 10
        self.alarms_repetition = []

        self.active = True
        self.ringing = False

    def set_event(self, is_alarm, event):

        self.is_alarm = is_alarm
        self.event = event

        self.format_data()
        self.set_alarm_repetition()

    def format_data(self):

        if self.event.kind == 'Hour':
            self.title = "{} - {}:{:0>2d}".format(self.event.title, self.event.start.hour, self.event.start.minute)

            # Set radio
            self.set_radio(extract_information_with_hashtag(self.event.description, "#radio"))

            # Set repetition: Extract the digit of the repetition text
            text_repetition = extract_information_with_hashtag(self.event.description, "#repetition")
            digits_pattern = "([0-9]{1,2})"
            digits_search = re.search(digits_pattern, text_repetition)
            if len(text_repetition) > 0 and digits_search:
                self.set_repetition(digits_search.group(1))
            else:
                logger.debug("There is no #repetition of no digits")

        elif self.event.kind == 'Day':
            self.title = self.event.title
        else:
            self.title = ''

    def set_radio(self, radio_str):

        if len(radio_str) > 0:
            logger.info("Set radio from %s to %s", self.radio, radio_str)
            self.radio = radio_str

    def set_repetition(self, repetition_value):

        if len(repetition_value) > 0:
            logger.info("Set number of repetition from %s to %s", self.repetition, repetition_value)
            self.repetition = int(repetition_value)

    def is_ringing(self, current_datetime):
        if self.event.start <= current_datetime <= self.event.end:
            if self.active is True:
                if self.ringing is False:
                    if current_datetime.replace(second=0, microsecond=0) in self.alarms_repetition:
                        self.ringing = True
                        self.alarms_repetition.pop(0)  # Remove first alarm to avoid new alarm for the same datetime
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
            self.alarms_repetition = []  # Reset alarms

            repet_datetime = self.event.start
            while repet_datetime < self.event.end:
                self.alarms_repetition.append(repet_datetime)
                repet_datetime += timedelta(minutes=self.repetition)

    def clear_event(self):
        logger.debug("Clear event")
        self.event = Event([], 'no_calendar', 'no_name')

        self.is_alarm = False
        self.title = ''
        self.radio = 'nrj'
        self.repetition = 10
        self.alarms_repetition = []

        self.active = True
        self.ringing = False


class Event:
    def __init__(self, calendar_item, calendar_name, name):

        self.calendar_name = calendar_name
        self.name = name

        if len(calendar_item) == 0:
            self.kind = 'None'  # 'None', 'Hour', 'Day'
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
