from datetime import datetime, timedelta
from notifications import *
from events import Event

my_notifs = Notifications()


def setup_function():
    my_notifs.clear()

def test_notifications():

    assert my_notifs.wifi is False
    assert my_notifs.alarm is False
    assert my_notifs.calendar_intervention is False

def test_set_wifi():
    assert my_notifs.wifi is False

    my_notifs.set_wifi(True)
    assert my_notifs.wifi is True
    my_notifs.set_wifi(False)
    assert my_notifs.wifi is False

def test_set_alarm():
    assert my_notifs.alarm is False

    my_notifs.set_alarm(True)
    assert my_notifs.alarm is True
    my_notifs.set_alarm(False)
    assert my_notifs.alarm is False

def test_set_calendar_intervention():
    assert my_notifs.calendar_intervention is False

    my_notifs.set_calendar_intervention(True)
    assert my_notifs.calendar_intervention is True
    my_notifs.set_calendar_intervention(False)
    assert my_notifs.calendar_intervention is False

def test_define_alarm_notif_no_event():
    event_today = Event([], 'calendar_name_test', False)
    event_tomorrow = Event([], 'calendar_name_test', False)

    one_date = datetime(2020, 3, 30)
    my_notifs.define_alarm_notif(one_date, event_today, event_tomorrow)
    assert my_notifs.alarm is False

def test_define_alarm_notif_today_alarm_before_end():

    one_date = datetime(2020, 3, 30)

    event_today = Event([], 'calendar_name_test', False)
    event_today.set_params({'kind': 'Hour', 'is_alarm': True, 'end': one_date+timedelta(hours=1)})
    event_tomorrow = Event([], 'calendar_name_test', False)

    my_notifs.define_alarm_notif(one_date, event_today, event_tomorrow)
    assert my_notifs.alarm is True

def test_define_alarm_notif_today_alarm_after_end():
    one_date = datetime(2020, 3, 30)

    event_today = Event([], 'calendar_name_test', False)
    event_today.set_params({'kind': 'Hour', 'is_alarm': True, 'end': one_date + timedelta(hours=1)})
    event_tomorrow = Event([], 'calendar_name_test', False)

    my_notifs.define_alarm_notif(one_date + timedelta(hours=2), event_today, event_tomorrow)
    assert my_notifs.alarm is False

    event_tomorrow = Event([], 'calendar_name_test', False)
    event_tomorrow.set_params({'is_alarm': True})
    my_notifs.define_alarm_notif(one_date + timedelta(hours=2), event_today, event_tomorrow)
    assert my_notifs.alarm is True

def test_define_alarm_notif_today_no_alarm_before_end():
    one_date = datetime(2020, 3, 30)

    event_today = Event([], 'calendar_name_test', False)
    event_today.set_params({'kind': 'Hour', 'is_alarm': False, 'end': one_date + timedelta(hours=1)})
    event_tomorrow = Event([], 'calendar_name_test', False)

    my_notifs.define_alarm_notif(one_date, event_today, event_tomorrow)
    assert my_notifs.alarm is False

def test_define_alarm_notif_today_no_alarm_tomorrow_alarm():
    one_date = datetime(2020, 3, 30)

    event_today = Event([], 'calendar_name_test', False)
    event_today.set_params({'kind': 'Day', 'is_alarm': False})
    event_tomorrow = Event([], 'calendar_name_test', False)
    event_tomorrow.set_params({'is_alarm': True})

    my_notifs.define_alarm_notif(one_date, event_today, event_tomorrow)
    assert my_notifs.alarm is False

    my_notifs.define_alarm_notif(one_date + timedelta(hours=14), event_today, event_tomorrow)
    assert my_notifs.alarm is True

def test_define_alarm_notif_today_change_limit_hour():
    one_date = datetime(2020, 3, 30)

    event_today = Event([], 'calendar_name_test', False)
    event_today.set_params({'kind': 'Day', 'is_alarm': False})
    event_tomorrow = Event([], 'calendar_name_test', False)
    event_tomorrow.set_params({'is_alarm': True})

    my_notifs.define_alarm_notif(one_date + timedelta(hours=14), event_today, event_tomorrow, limit_hour=18)
    assert my_notifs.alarm is False

    my_notifs.define_alarm_notif(one_date + timedelta(hours=18), event_today, event_tomorrow)
    assert my_notifs.alarm is True

def test_define_calendar_intervention_notif_no_events():
    events = [Event([], 'calendar_name_test', False)]*3

    my_notifs.define_calendar_intervention_notif(events)
    assert my_notifs.calendar_intervention is False

def test_define_calendar_intervention_notif_alarm_first():
    event1 = Event([], 'calendar_name_test', False)
    event1.set_params({'kind': 'Hour', 'is_alarm': True})
    event2 = Event([], 'calendar_name_test', False)
    event3 = Event([], 'calendar_name_test', False)
    events = [event1, event2, event3]

    my_notifs.define_calendar_intervention_notif(events)
    assert my_notifs.calendar_intervention is False

def test_define_calendar_intervention_notif_alarm_second():
    event1 = Event([], 'calendar_name_test', False)
    event1.set_params({'kind': 'Hour', 'is_alarm': True})
    event2 = Event([], 'calendar_name_test', False)
    event3 = Event([], 'calendar_name_test', False)
    events = [event2, event1, event3]

    my_notifs.define_calendar_intervention_notif(events)
    assert my_notifs.calendar_intervention is True

def test_get_values():

    my_notifs.set_wifi(True)
    my_notifs.set_alarm(False)
    my_notifs.set_calendar_intervention(True)

    values = my_notifs.get_values()

    assert values['wifi'] is True
    assert values['alarm'] is False
    assert values['calendar_intervention'] is True

def test_clear():

    my_notifs.set_wifi(True)
    my_notifs.set_alarm(True)
    my_notifs.set_calendar_intervention(True)

    my_notifs.clear()

    assert my_notifs.wifi is False
    assert my_notifs.alarm is False
    assert my_notifs.calendar_intervention is False