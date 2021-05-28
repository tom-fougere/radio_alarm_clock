from calendarAPI import *
from events import sort_events, FORCE_STRING
import logging

logger = logging.getLogger("radioAlarmLogger")

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

    def force_alarm(self, current_datetime):
        """
        Force the alarm. Add #force at the beginning of the summary of the event in the Alarm Calendar
        :param current_datetime: Current datetime
        """
        # Get events from 'alarm calendar'
        events = self.google_service.get_events_from_day(self.alarm_calendar, current_datetime, reset_hour=True)

        if len(events['items'][0]) > 0:
            for i_event in events['items']:

                # Add hashtag to the summary
                i_event['summary'] = ' '.join([FORCE_STRING, i_event['summary']])

                # Update event
                self.google_service.update_event(i_event, calendar_id=self.alarm_calendar)

                logger.info('Add "%s" to all alarms')
        else:
            logger.warning('No possibility to force the alarm because there is none !')




