from dateTime import *
import datetime
import time


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
    assert os_datetime.get_datetime_string() == now_string


def test_ntp_datetime():
    ntp_datetime = NTPDate()

    now = datetime.datetime.now()
    now_string = "%04d/%02d/%02d %02d:%02d:%02d" % (now.year,
                                                    now.month,
                                                    now.day,
                                                    now.hour,
                                                    now.minute,
                                                    now.second)

    assert ntp_datetime.get_year() == now.year
    assert ntp_datetime.get_month() == now.month
    assert ntp_datetime.get_day() == now.day
    assert ntp_datetime.get_hour() == now.hour
    assert ntp_datetime.get_minute() == now.minute
    assert ntp_datetime.get_datetime_string() == now_string


def test_update_time():
    os_datetime = OSDate()
    ntp_datetime = NTPDate()

    os_datetime_seconds1 = os_datetime.get_hour()*3600 + \
                           os_datetime.get_minute()*60 + \
                           os_datetime.get_second()

    ntp_datetime_seconds1 = ntp_datetime.get_hour()*3600 + \
                            ntp_datetime.get_minute()*60 + \
                            ntp_datetime.get_second()

    assert os_datetime_seconds1 == ntp_datetime_seconds1

    # Wait few seconds
    time.sleep(2)

    os_datetime.update()
    ntp_datetime.update()

    os_datetime_seconds2 = os_datetime.get_hour() * 3600 + \
                           os_datetime.get_minute() * 60 + \
                           os_datetime.get_second()

    ntp_datetime_seconds2 = ntp_datetime.get_hour() * 3600 + \
                            ntp_datetime.get_minute() * 60 + \
                            ntp_datetime.get_second()

    assert os_datetime_seconds1 < os_datetime_seconds2
    assert ntp_datetime_seconds1 < ntp_datetime_seconds2
