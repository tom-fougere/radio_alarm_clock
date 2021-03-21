from dateTime import OSDate
from urllib2 import urlopen, URLError, HTTPError
import time
import socket


class InternetChecker:
    def __init__(self):
        self.url = 'https://google.com/'
        self.url_start = 'https://www.google'
        self.logFile = 'internet_connection.txt'
        self.numberOfTests = 4

    def check_connection(self):
        socket.setdefaulttimeout(23)

        index = 0
        good_connection = 0
        while index <= self.numberOfTests:
            try:
                response = urlopen(self.url)
            except (HTTPError, URLError):
                self.internet_down()
            else:
                response.read()
                if response.url.startswith(self.url_start):
                    good_connection += 1
                else:
                    self.internet_down()

            index += 1
            time.sleep(0.5)

        if good_connection == 5:
            print("Internet Connected")
            return True
        else:
            print('At least one connection error')
            return False

    def internet_down(self):
        print("Internet Down")
        current_time = OSDate()
        ct = current_time.get_datetime()
        f = open(self.logFile, 'a')
        f.write("%s\n" % ct)
        f.close()
