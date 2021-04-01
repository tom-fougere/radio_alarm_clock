from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import time
import socket


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

            # Sleep
            time.sleep(self.duration_check_connection/self.number_of_tests)

        if nb_connection == self.number_of_tests:
            print("Internet Connected")
            return True
        else:
            print(str(self.number_of_tests - nb_connection), '/', str(nb_connection), 'connection errors')
            return False

    def check_connection_once(self):
        try:
            response = urlopen(self.url)
        except (HTTPError, URLError):
            connected = False
        else:
            response.read()
            if response.url.startswith(self.url_start):
                connected = True
            else:
                connected = False
        return connected
