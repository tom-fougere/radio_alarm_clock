from datetime import timedelta
import re
import logging

from events import Event


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

    def set_event(self, event):

        self.event = event
        self.is_alarm = event.is_alarm

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

        else:
            self.title = self.event.title

    def set_radio(self, radio_str):

        if len(radio_str) > 0:
            logger.info("Set radio from %s to %s", self.radio, radio_str)
            self.radio = radio_str

    def set_repetition(self, repetition_value):

        if len(repetition_value) > 0:
            logger.info("Set number of repetition from %s to %s", self.repetition, repetition_value)
            self.repetition = int(repetition_value)

    def is_ringing(self, current_datetime):
        if self.is_alarm is True and self.event.start <= current_datetime <= self.event.end:
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