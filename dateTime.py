from InternetCheck import InternetChecker

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
        self.currentDatetime = datetime.min

    @abstractmethod
    def update(self):
        pass

    def get_year(self):
        return self.currentDatetime.year

    def get_month(self):
        return self.currentDatetime.month

    def get_day(self):
        return self.currentDatetime.day

    def get_hour(self):
        return self.currentDatetime.hour

    def get_minute(self):
        return self.currentDatetime.minute

    def get_second(self):
        return self.currentDatetime.second

    def get_weekday(self):
        return self.currentDatetime.isoweekday()

    def get_week_of_the_year(self):
        return self.currentDatetime.isocalendar()[1]

    def get_day_of_the_year(self):
        return self.currentDatetime.timetuple().tm_yday

    def display_date(self):
        print("%04d/%02d/%02d" % (self.currentDatetime.year, self.currentDatetime.month, self.currentDatetime.day))

    def display_time(self):
        print("%02d:%02d" % (self.currentDatetime.hour, self.currentDatetime.minute))

    def get_datetime(self):
        return self.currentDatetime

    def get_datetime_string(self):
        current_datetime = "%04d/%02d/%02d %02d:%02d:%02d" % (self.currentDatetime.year,
                                                              self.currentDatetime.month,
                                                              self.currentDatetime.day,
                                                              self.currentDatetime.hour,
                                                              self.currentDatetime.minute,
                                                              self.currentDatetime.second)
        return current_datetime


class OSDate(CurrentDate):

    def __init__(self):
        self.currentDatetime = datetime.datetime.now()

    def update(self):
        self.currentDatetime = datetime.datetime.now()


class NTPDate(CurrentDate):

    def __init__(self):

        self.currentDatetime = get_internet_datetime()

    def update(self):

        self.currentDatetime = get_internet_datetime()


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


