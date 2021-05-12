# External packages
import logging
import os

# Personal pacjages
from documents.rw_dict import *


RADIO_URL_FILE = 'documents/radio_url.txt'
MP3_KEY = 'mp3'
logger = logging.getLogger("radioAlarmLogger")


class Radio:
    def __init__(self):
        self.radio = ''
        self.url = ''
        self.on = False

    def turn_on(self):
        """
        Turn on the radio
        """
        os.system(' '.join(["mpg321", self.url, '&']))
        self.on = True

    def turn_off(self):
        """
        Trun off the radio
        """

        # Force mpg321 to stop
        os.system(' '.join(['pkill', 'mpg321']))

        self.on = False

    def set_radio_url(self, radio):
        """
        Set the url of the selected radio

        :param radio: wanted radio, string
        """

        radio_url_dict = read_dict_file(RADIO_URL_FILE)

        if radio.lower() in radio_url_dict.keys():
            logger.debug('The radio url is changed')
            self.radio = radio.lower()
            self.url = radio_url_dict[radio.lower()]
        else:
            logger.warning('The radio doesn\'t exist in the dictionary')

    def set_mp3_music(self):
        """
        Set mp3 file instead of radio url
        """

        logger.debug('The radio url is changed')
        radio_url_dict = read_dict_file(RADIO_URL_FILE)
        self.url = radio_url_dict[MP3_KEY]


