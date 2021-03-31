from dateTime import *
import datetime


def test_os_datetime():
    os_datetime = OSDate()

    now = datetime.datetime.now()
    now_string = "%04d/%02d/%02d %02d:%02d:%02d" % (now.year,
                                                    now.month,
                                                    now.day,
                                                    now.hour,
                                                    now.minute,
                                                    now.second)

    assert os_datetime.get_year() == now.year
    assert os_datetime.get_month() == now.month
    assert os_datetime.get_day() == now.day
    assert os_datetime.get_hour() == now.hour
    assert os_datetime.get_minute() == now.minute
    assert os_datetime.get_datetime() == now_string


def test_ntp_datetime():
    os_datetime = NTPDate()

    now = datetime.datetime.now()
    now_string = "%04d/%02d/%02d %02d:%02d:%02d" % (now.year,
                                                    now.month,
                                                    now.day,
                                                    now.hour,
                                                    now.minute,
                                                    now.second)

    assert os_datetime.get_year() == now.year
    assert os_datetime.get_month() == now.month
    assert os_datetime.get_day() == now.day
    assert os_datetime.get_hour() == now.hour
    assert os_datetime.get_minute() == now.minute
    assert os_datetime.get_datetime() == now_string
