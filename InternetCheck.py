from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import time
import socket
import logging

logger = logging.getLogger("radioAlarmLogger")


class InternetChecker:
    def __init__(self):
        self.url = 'https://google.com/'
        self.url_start = 'https://www.google'
        self.duration_check_connection = 2  # seconds
        self.number_of_tests = 4

    def is_connected(self):
        socket.setdefaulttimeout(23)

        nb_connection = 0
        for i_test in range(self.number_of_tests):

            # Count the number of correct connection
            is_connected = self.check_connection_once()
            if is_connected:
                nb_connection += 1
            logger.info('Test %s/%s - Successful connection: %s/%s',
                        i_test, self.number_of_tests, nb_connection, self.number_of_tests)

            # Sleep
            time.sleep(self.duration_check_connection/self.number_of_tests)

        if nb_connection == self.number_of_tests:
            logger.info("Internet Connected")
            return True
        else:
            logger.warning('Internet not connected: %s/%s connection errors !', self.number_of_tests - nb_connection)
            return False

    def check_connection_once(self):
        try:
            response = urlopen(self.url)
            logger.debug('Try connexion once (response:%s)', response.url)
        except (HTTPError, URLError):
            connected = False
        else:
            response.read()
            if response.url.startswith(self.url_start):
                connected = True
            else:
                connected = False
        return connected
