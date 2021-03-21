import datetime
from socket import AF_INET, SOCK_DGRAM
import socket
import struct
import time


class OSDate:

    def __init__(self):
        self.currentDatetime = datetime.datetime.now()

    def update(self):
        self.currentDatetime = datetime.datetime.now()

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
        current_datetime = "%04d/%02d/%02d %02d:%02d:%02d" % (self.currentDatetime.year,
                                                              self.currentDatetime.month,
                                                              self.currentDatetime.day,
                                                              self.currentDatetime.hour,
                                                              self.currentDatetime.minute,
                                                              self.currentDatetime.second)
        return current_datetime


class NTPDate:
    # NTP server
    host = "0.fr.pool.ntp.org"

    # reference time (in seconds since 1900-01-01 00:00:00)
    TIME1970 = 2208988800  # 1970-01-01 00:00:00

    # others parameters
    port = 123
    buf = 1024
    address = (host, port)
    msg = '\x1b' + 47 * '\0'

    def __init__(self):
        # connect to server
        client = socket.socket(AF_INET, SOCK_DGRAM)
        client.sendto(NTPDate.msg, NTPDate.address)
        msg, address = client.recvfrom(NTPDate.buf)

        t = struct.unpack("!12I", msg)[10]
        t -= NTPDate.TIME1970

        # self.currentDatetime = time.ctime(t)
        self.currentDatetime = datetime.datetime.strptime(time.ctime(t), "%a %b %d %H:%M:%S %Y")

    def update(self):
        # connect to server
        client = socket.socket(AF_INET, SOCK_DGRAM)
        client.sendto(NTPDate.msg, NTPDate.address)
        msg, address = client.recvfrom(NTPDate.buf)

        t = struct.unpack("!12I", msg)[10]
        t -= NTPDate.TIME1970

        self.currentDatetime = datetime.datetime.strptime(time.ctime(t), "%a %b %d %H:%M:%S %Y")

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
