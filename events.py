from datetime import datetime, timedelta
import re

import logging


logger = logging.getLogger("radioAlarmLogger")


class Event:
    def __init__(self):
        self.raw = dict()

        self.id = ''
        self.is_alarm = False
        self.title = ''
        self.start_time = datetime.min
        self.end_time = datetime.min
        self.alarms = []
        self.radio = 'nrj'
        self.repetition = 10

        self.active = False
        self.ringing = False

    def set_event(self, is_alarm, event):

        self.is_alarm = is_alarm
        self.active = self.is_alarm

        if event is not None:
            self.id = event['id']

            self.raw['start'] = event['start']['dateTime']
            self.raw['end'] = event['end']['dateTime']
            self.raw['summary'] = event['summary']
            try:
                self.raw['description'] = event['description']
            except KeyError:
                self.raw['description'] = ''
                logger.debug('No description field in event')

            self.format_data()
            self.set_alarm_repetition()
        else:
            logger.debug('No event')

    def format_data(self):

        # Set the title as the summary of the event removing the hashtag key
        hashtag_pattern = r"^(#[a-zA-Z]+) ([a-zA-Z\w ]+)"
        hashtag_search = re.search(hashtag_pattern, self.raw['summary'])
        if hashtag_search:
            self.title = hashtag_search.group(2)
        else:
            self.title = self.raw['summary']

        # Set the start/end time as datetime (Remove useless timezone)
        self.start_time = datetime.strptime(self.raw['start'], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
        self.end_time = datetime.strptime(self.raw['end'], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)

        # Set radio
        self.set_radio(extract_information_with_hashtag(self.raw['description'] + '#', "#radio"))

        # Set repetition: Extract the digit of the repetition text
        text_repetition = extract_information_with_hashtag(self.raw['description'] + '#', "#repetition")
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
                    if current_datetime in self.alarms:
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

            repet_datetime = self.start_time
            while repet_datetime < self.end_time:
                self.alarms.append(repet_datetime)
                repet_datetime += timedelta(minutes=self.repetition)

    def clear_event(self):
        logger.debug("Clear event")
        self.raw = dict()

        self.id = ''
        self.is_alarm = False
        self.title = ''
        self.start_time = datetime.min
        self.end_time = datetime.min
        self.alarms = []
        self.radio = 'nrj'
        self.repetition = 10

        self.active = False
        self.ringing = False


def extract_information_with_hashtag(full_text, hashtag):
    """
    Extract text after a defined hashtag
    :param full_text: Text with hashtag and needed information, string
    :param hashtag: Hashtag to search, string, example: #radio
    :return:
        - information: Information after a hashtag
    """

    # Search hashtag key
    index_defined_hashtag = full_text.find(hashtag)
    index_next_hashtag = full_text.find('#', index_defined_hashtag + 1)

    # Extract information and remove '\n' character
    information = full_text[index_defined_hashtag + len(hashtag) + 1: index_next_hashtag]
    information = information.rstrip()

    return information
