from calendarAPI import *

OFF_STRING = '[off]'
FORCE_STRING = '[force]'


class AlarmCalendar:

    def __init__(self):
        self.google_service = GoogleCalendarAPI()
        self.alarm_calendar = None
        self.public_holiday_calendar = None
        self.personal_calendar = None

        # Init google calendar service
        self.google_service.init_calendar_service()

    def set_calendars(self, alarm_calendar, public_holiday_calendar, personal_calendar):
        self.alarm_calendar = alarm_calendar
        self.public_holiday_calendar = public_holiday_calendar
        self.personal_calendar = personal_calendar

    def is_alarm_today(self, today_datetime):

        # Convert the datetime to string
        day, month, year = today_datetime.day, today_datetime.month, today_datetime.year
        day = str(day).zfill(2)
        month = str(month).zfill(2)
        year = str(year).zfill(4)

        # Get the events from the three calendars
        events_alarm_calendar = self.google_service.get_events_from_day(self.alarm_calendar,
                                                                        day=day,
                                                                        month=month,
                                                                        year=year)

        events_public_holiday_calendar = self.google_service.get_events_from_day(self.public_holiday_calendar,
                                                                                 day=day,
                                                                                 month=month,
                                                                                 year=year)

        events_personal_calendar = self.google_service.get_events_from_day(self.personal_calendar,
                                                                           day=day,
                                                                           month=month,
                                                                           year=year)

        # Sort the events to get the one that should trigger a ringing
        is_alarm_today, alarm_event = get_highest_priority_event(events_alarm_calendar, events_public_holiday_calendar, events_personal_calendar)

        return is_alarm_today, alarm_event


def get_first_event(events, priority_string=''):
    """
    Get the first event of a list of events
    If the event have the substring 'priority_string' in the name, it'll be selected

    :param events: List of Events, Google service "Event"
    :param priority_string: Substring to search in event name, string
    :return:
        - is_priority_event: Is the first element part of a priority, Boolean
        - event: First event, Google service "Event"
    """
    is_priority_event = False

    events_list = []

    for event in events['items']:
        if priority_string in event['summary'].lower():
            is_priority_event = True
            events_list.insert(0, event)
        else:
            events_list.append(event)

    event = events_list[0] if len(events_list) > 0 else []
    return is_priority_event, event


def get_highest_priority_event(events_alarm_calendar, events_public_holiday_calendar, events_personal_calendar):
    """
    Get the highest priority event in all calendars (alarm calendar, public holiday calendar et personal calendar)
    The highest priority event corresponds to the event where the alarm should ring

    :param events_alarm_calendar: List of Events from the alarm calendar, Google service "Event"
    :param events_public_holiday_calendar: List of Events from the public holiday calendar, Google service "Event"
    :param events_personal_calendar: List of Events from the personal calendar, Google service "Event"
    :return:
        - is_alarm_today: Is the event to trigger a ringing, Boolean
        - alarm_event: (Associated) Highest priority event, Google service "Event"
    """
    is_alarm = True if len(events_alarm_calendar['items']) > 0 else False
    is_force_alarm, force_event = get_first_event(events_alarm_calendar, FORCE_STRING)
    is_off_event, off_event = get_first_event(events_personal_calendar, OFF_STRING)
    is_public_holiday, public_holiday_event = get_first_event(events_public_holiday_calendar)

    is_alarm_today = is_force_alarm or (is_alarm and (not is_off_event and not is_public_holiday))

    alarm_event = None
    if is_force_alarm:
        alarm_event = force_event
    elif is_alarm and (not is_off_event and not is_public_holiday):
        alarm_event = events_alarm_calendar['items'][0]
    elif is_off_event:
        alarm_event = off_event
    elif is_public_holiday:
        alarm_event = public_holiday_event

    # Save the event from the personal calendar even if there is no alarm
    elif len(events_personal_calendar['items']) > 0:
        alarm_event = off_event

    # Save the event from the public holiday calendar even if there is no alarm
    elif len(events_public_holiday_calendar['items']) > 0:
        alarm_event = public_holiday_event

    return is_alarm_today, alarm_event

