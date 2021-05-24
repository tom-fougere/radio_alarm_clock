from calendarAPI import *
from events import convert_google_events_to_calendar_events
import logging

OFF_STRING = '#off'
FORCE_STRING = '#force'

logger = logging.getLogger(__name__)

class AlarmCalendar:

    def __init__(self):
        self.google_service = GoogleCalendarAPI()
        self.alarm_calendar = None
        self.public_holiday_calendar = None
        self.personal_calendar = None

        # Init google calendar service
        self.google_service.init_calendar_service()

    def set_calendars(self, alarm_calendar, public_holiday_calendar, personal_calendar):
        """
        Set calendars to monitor

        :param alarm_calendar: Specific calendar of alarms
        :param public_holiday_calendar: Specific calendar of public holiday
        :param personal_calendar: Personal calendar
        """
        self.alarm_calendar = alarm_calendar
        self.public_holiday_calendar = public_holiday_calendar
        self.personal_calendar = personal_calendar

    def is_alarm_today(self, today_datetime, reset_hour=False):
        """
        Check in calendars if there is an alarm today
        Search alarms in calendars after the selected datetime

        :param today_datetime: Current datetime
        :param reset_hour: If True, the hour is not taken into account
        :return:
            - is_alarm_today: boolean for alarm to the selected datetime
            - alarm_event: alarm associated
        """

        # Get the events from the three calendars
        events_alarm_calendar = self.google_service.get_events_from_day(self.alarm_calendar,
                                                                        today_datetime,
                                                                        reset_hour=reset_hour)

        events_public_holiday_calendar = self.google_service.get_events_from_day(self.public_holiday_calendar,
                                                                                 today_datetime)

        events_personal_calendar = self.google_service.get_events_from_day(self.personal_calendar,
                                                                           today_datetime)

        # logger.debug('Events from Alarm calendar (%s): %s', today_datetime, events_alarm_calendar)
        # logger.debug('Events from Public Holiday calendar (%s): %s', today_datetime, events_public_holiday_calendar)
        # logger.debug('Events from Personal calendar (%s): %s', today_datetime, events_personal_calendar)

        sorted_events = sort_events(events_alarm_calendar, events_public_holiday_calendar, events_personal_calendar)
        logger.debug('Sorted Events from Google calendars (%s): %s', today_datetime, sorted_events)

        is_alarm_today = []
        for event in sorted_events:
            if event.name == 'Alarm':
                is_alarm_today.append(True)
            else:
                is_alarm_today.append(False)

        return is_alarm_today, sorted_events

    def is_alarm_tomorrow(self, today_datetime):
        """
        Check in calendars if there is an alarm the day of the selected datetime
        Search alarms in calendars after the selected datetime

        :param today_datetime: Current datetime
        :param reset_hour: If True, the hour is not taken into account
        :return:
            - is_alarm_today: boolean for alarm to the selected datetime
            - alarm_event: alarm associated
        """

        tomorrow_datetime = today_datetime + datetime.timedelta(days=1)

        is_alarm_tomorrow, alarm_event = self.is_alarm_today(tomorrow_datetime, reset_hour=True)

        return is_alarm_tomorrow, alarm_event


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

def sort_events(events_alarm_calendar, events_public_holiday_calendar, events_personal_calendar):
    """
    Sort events from 3 google calendars (alarm, public holiday and personal)
    order: #force, #off, public holiday, alarm, personal
    :param events_alarm_calendar: List of Events from the alarm calendar, Google service "Event"
    :param events_public_holiday_calendar: List of Events from the public holiday calendar, Google service "Event"
    :param events_personal_calendar: List of Events from the personal calendar, Google service "Event"
    :return:
        - list of sorted CalendarEvent
    """

    alarm_calendar_name = 'Alarm'
    public_holiday_calendar_name = 'Public Holiday'
    personal_calendar_name = 'Personal'

    events_alarm = convert_google_events_to_calendar_events(events_alarm_calendar, name=alarm_calendar_name)
    events_public_holiday = convert_google_events_to_calendar_events(events_public_holiday_calendar, name=public_holiday_calendar_name)
    events_personal = convert_google_events_to_calendar_events(events_personal_calendar, name=personal_calendar_name)

    full_list = events_alarm + events_public_holiday + events_personal
    sorted_events = []

    priority = 0
    index = 0
    while len(full_list) > 0:
        event = full_list[index]

        if priority == 0:
            if event.title.lower().find(FORCE_STRING)>=0:  # FORCE
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        if priority == 1:
            if event.title.lower().find(OFF_STRING) >= 0:  # OFF
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        if priority == 2:
            if event.name == public_holiday_calendar_name:
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        if priority == 3:
            if event.name == alarm_calendar_name:
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        if priority == 4:
            if event.name == personal_calendar_name:
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1

        if index >= len(full_list):
            priority +=1
            index = 0

    return sorted_events



