from abc import ABC, abstractmethod
import datetime
from socket import AF_INET, SOCK_DGRAM
import socket
import struct
import time

SECOND_MARGIN = 1

# NTP server
NTP_SERVER = dict()
NTP_SERVER['host'] = "0.fr.pool.ntp.org"
NTP_SERVER['time1970'] = 2208988800  # reference time (in seconds since 1900-01-01 00:00:00)
NTP_SERVER['port'] = 123
NTP_SERVER['buf'] = 1024
NTP_SERVER['address'] = (NTP_SERVER['host'], NTP_SERVER['port'])
NTP_SERVER['msg'] = b'\x1b' + 47 * b'\0'


class CurrentDate(ABC):

    @abstractmethod
    def __init__(self):
        self.current_datetime = datetime.min

    @abstractmethod
    def update(self):
        pass

    def get_year(self):
        return self.current_datetime.year

    def get_month(self):
        return self.current_datetime.month

    def get_day(self):
        return self.current_datetime.day

    def get_hour(self):
        return self.current_datetime.hour

    def get_minute(self):
        return self.current_datetime.minute

    def get_second(self):
        return self.current_datetime.second

    def get_weekday(self):
        return self.current_datetime.isoweekday()

    def get_week_of_the_year(self):
        return self.current_datetime.isocalendar()[1]

    def get_day_of_the_year(self):
        return self.current_datetime.timetuple().tm_yday

    def display_date(self):
        print("%04d/%02d/%02d" % (self.current_datetime.year, self.current_datetime.month, self.current_datetime.day))

    def display_time(self):
        print("%02d:%02d" % (self.current_datetime.hour, self.current_datetime.minute))

    def get_datetime(self):
        return self.current_datetime

    def get_datetime_string(self):
        current_datetime = "%04d/%02d/%02d %02d:%02d:%02d" % (self.current_datetime.year,
                                                              self.current_datetime.month,
                                                              self.current_datetime.day,
                                                              self.current_datetime.hour,
                                                              self.current_datetime.minute,
                                                              self.current_datetime.second)
        return current_datetime


class OSDate(CurrentDate):

    def __init__(self):
        self.current_datetime = datetime.datetime.now()

    def update(self):
        self.current_datetime = datetime.datetime.now()


class NTPDate(CurrentDate):

    def __init__(self):

        self.current_datetime = get_internet_datetime()

    def update(self):

        self.current_datetime = get_internet_datetime()


def get_internet_datetime(parameters=NTP_SERVER):
    """
    Connect to a server (NTP) to get the time with internet

    :param parameters: parameters of the server, dict
    :return:
        - datetime
    """
    # connect to server
    client = socket.socket(AF_INET, SOCK_DGRAM)
    client.sendto(parameters['msg'], parameters['address'])
    msg, address = client.recvfrom(parameters['buf'])

    t = struct.unpack("!12I", msg)[10]
    t -= parameters['time1970']

    return datetime.datetime.strptime(time.ctime(t), "%a %b %d %H:%M:%S %Y")


class ReliableDate(CurrentDate):

    def __init__(self):
        self.os_date = OSDate()

        try:
            self.ntp_date = NTPDate()
            self.current_datetime = self.ntp_date.get_datetime()
        except():
            self.ntp_date = None
            self.current_datetime = self.os_date.get_datetime()

        # Save the date of the init to check internet connection regularly
        self.save_datetime = self.current_datetime
        self.need_cycle_double_check = True

    def update(self, check_internet_connection=False):

        self.os_date.update()
        try:
            self.ntp_date.update()
            self.current_datetime = self.ntp_date.get_datetime()
        except():
            self.current_datetime = self.os_date.get_datetime()

    def is_consistent_datetime(self):
        return abs((self.ntp_date.get_datetime() - self.os_date.get_datetime()).total_seconds()) < SECOND_MARGIN


