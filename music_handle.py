# External packages
import logging
import subprocess

# Personal pacjages
from documents.rw_dict import read_dict_file


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
        subprocess.call(["mpg321", self.url])
        self.on = True

    def turn_off(self):
        """
        Trun off the radio
        """

        # Search job dedicated to mpg321
        out = subprocess.Popen(["jobs"])
        stdout, stderr = out.communicate()

        job_id = stdout.split()[0]

        # Kill job dedicated to mpg321
        subprocess.call(["kill", "%" + job_id])

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


