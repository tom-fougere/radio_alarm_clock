from calendarAPI import *
from events import convert_google_events_to_calendar_events
import logging

OFF_STRING = '#off'
FORCE_STRING = '#force'

logger = logging.getLogger(__name__)

class OnlineCalendar:

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
            - alarm_event: first (sorted) event of the date
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

        is_alarm_today = False
        if len(sorted_events) > 0 and sorted_events[0].name == 'Alarm':
            is_alarm_today = True

        return is_alarm_today, sorted_events[0]

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

    def get_events(self, today_datetime, reset_hour=False):
        """
        Get events from the 3 calendars at the specified datetime

        :param today_datetime: Current datetime
        :param reset_hour: If True, the hour is not taken into account
        :return:
            - sorted_events: list of events, Events
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

        return sorted_events


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

    full_list = events_public_holiday + events_alarm + events_personal
    sorted_events = []

    priority = 0
    index = 0
    while len(full_list) > 0:
        event = full_list[index]

        if event.kind == 'None' and priority < 5:
            index +=1
        elif priority == 0:
            if event.title.lower().find(FORCE_STRING)>=0:  # FORCE
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        elif priority == 1:
            if event.title.lower().find(OFF_STRING) >= 0:  # OFF
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        elif priority == 2:
            if event.name == public_holiday_calendar_name:
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        elif priority == 3:
            if event.name == alarm_calendar_name:
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        elif priority == 4:
            if event.name == personal_calendar_name:
                sorted_events.append(event)
                full_list.pop(index)
            else:
                index += 1
        if priority == 5:
            sorted_events.append(event)
            full_list.pop(index)

        if index >= len(full_list):
            priority +=1
            index = 0

    return sorted_events



