# External packages
import logging
import os

# Personal packages
from documents.rw_dict import *


RADIO_URL_FILE = 'musics/radio_url.txt'
MP3_FOLDER = 'musics/'
MP3_KEY = 'mp3'
logger = logging.getLogger("radioAlarmLogger")


class Radio:
    def __init__(self):
        self.radio = ''
        self.on = False

    def turn_on(self, is_internet_ok=True):
        """
        Turn on the radio
        """
        radio_url_dict = read_dict_file(RADIO_URL_FILE)

        if is_internet_ok is True:
            music_link = radio_url_dict[self.radio.lower()]
        else:
            logger.warning('Internet is down: MP3 is used for the music')
            music_link = ''.join([MP3_FOLDER, radio_url_dict[MP3_KEY]])

        # Turn on the music
        os.system(' '.join(["mpg321", music_link, '&']))
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
        else:
            logger.warning('The radio doesn\'t exist in the dictionary')



