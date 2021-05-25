from epaper_display import *
from events import Event

from datetime import datetime, timedelta

display_test = EPaper()
event_today = Event([], 'no_calendar', 'no_name')
event_tomorrow = Event([], 'no_calendar', 'no_name')

def setup_function():
    display_test.is_full_updated = False

def test_need_full_update():
    now = datetime(2021, 4, 19, 20, 00, 00)
    display_test.hour = 20
    display_test.minute = 0

    one_datetime = now + timedelta(minutes=59)
    assert display_test.need_full_update(one_datetime) == False

    one_datetime = now + timedelta(minutes=60)
    assert display_test.need_full_update(one_datetime) == True


def test_need_new_screen():
    now = datetime(2021, 4, 19, 20, 00, 00)
    display_test.hour = 20
    display_test.minute = 0

    one_datetime = now + timedelta(seconds=59)
    assert display_test.need_new_screen(one_datetime) == False

    one_datetime = now + timedelta(seconds=60)
    assert display_test.need_new_screen(one_datetime) == True

    one_datetime = now + timedelta(minutes=1)
    assert display_test.need_new_screen(one_datetime) == True

def test_update():
    now = datetime(2021, 4, 19, 20, 00, 00)
    display_test.hour = 20
    display_test.minute = 0

    # Few seconds later
    one_datetime = now + timedelta(seconds=5)
    display_test.update(one_datetime, event_today, event_tomorrow, is_wifi_on=True, is_alarm_on=False)

    assert display_test.is_full_updated is False
    assert display_test.hour == 20
    assert display_test.minute == 0

    # One minute later
    one_datetime = now + timedelta(seconds=65)
    display_test.update(one_datetime, event_today, event_tomorrow, is_wifi_on=True, is_alarm_on=False)

    assert display_test.is_full_updated is False
    assert display_test.hour == 20
    assert display_test.minute == 1

    # One hour later
    one_datetime = now + timedelta(minutes=65)
    display_test.update(one_datetime, event_today, event_tomorrow, is_wifi_on=True, is_alarm_on=False)

    assert display_test.is_full_updated is True
    assert display_test.hour == 21
    assert display_test.minute == 5

    # One hour and one minute later
    one_datetime = now + timedelta(minutes=66)
    display_test.update(one_datetime, event_today, event_tomorrow, is_wifi_on=True, is_alarm_on=False)

    assert display_test.is_full_updated is False
    assert display_test.hour == 21
    assert display_test.minute == 6

    # One hour and 2 minutes later + force update
    one_datetime = now + timedelta(minutes=67)

    event_today.set_params({'start':datetime(2021, 4, 19, 23, 00, 00), 'end':datetime(2021, 4, 19, 23, 30, 00)})
    display_test.update(one_datetime, event_today, event_tomorrow, force_update=True, is_alarm_on=True)

    assert display_test.is_full_updated is True
    assert display_test.hour == 21
    assert display_test.minute == 7


