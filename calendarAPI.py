import datetime
import pytz
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import logging

logger = logging.getLogger("radioAlarmLogger")

# If modifying these scopes, delete the file token.json.
SCOPES_DEFAULT = ['https://www.googleapis.com/auth/calendar.readonly']
SCOPES_EVENTS = ['https://www.googleapis.com/auth/calendar.events']

CREDENTIALS_FILE = 'documents/credentials.json'
TOKEN_JSON_FILE = 'documents/token.json'
TOKEN_EVENTS_JSON_FILE = 'documents/token_event.json'


class GoogleCalendarAPI:

    def __init__(self):
        self.credentials = None
        self.google_service = None

    def init_calendar_service(self):
        """
        Initialize the access to the Google Calendar API
        """
        self.set_credentials()
        self.build_google_service_access()

    def set_credentials(self, token_file=TOKEN_JSON_FILE, scopes=SCOPES_DEFAULT):
        """
        Set the credential to access Google Calendar API
        :param token_file: token of the Google Calendar API, string (path of file)
        :param scopes: scope 'authorization) of the Google Calendar API, string
        """
        self.credentials = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_file):
            self.credentials = Credentials.from_authorized_user_file(token_file, scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not self.credentials or not self.credentials.valid:
            logger.warning('Google Calendar API Credentials are no valid !')
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                logger.warning('Google Calendar API Credentials expired, refresh token !')
                self.credentials.refresh(Request())
            else:
                logger.error('Google Calendar API Window app needed !')
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, scopes)
                self.credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(self.credentials.to_json())

    def build_google_service_access(self):
        """
        Authorizing requests to the Google Calendar API
        """
        self.google_service = build('calendar', 'v3', credentials=self.credentials)

    def get_list_calendars_name(self):
        """
        Get the (summary) name of all calendars

        :return:
            - calendars_name (string): List of calendar's name
        """

        calendars_result = self.google_service.calendarList().list().execute()
        calendars_list = calendars_result.get('items', [])

        calendars_name = []
        for calendar in calendars_list:
            if 'summaryOverride' in calendar.keys():
                calendars_name.append(calendar['summaryOverride'])
            else:
                calendars_name.append(calendar['summary'])

        return calendars_name

    def get_list_calendars_id(self):
        """
        Get the id of all calendars

        :return:
            - calendars_id (string): List of calendar's id
        """

        calendars_result = self.google_service.calendarList().list().execute()
        calendars_list = calendars_result.get('items', [])

        calendars_id = [calendar['id'] for calendar in calendars_list]

        return calendars_id

    def get_events_from_day(self, calendar_id, today_datetime, reset_hour=False):
        """
        Get all events during a defined day (of a defined calendar)

        :param calendar_id: Calendar ID, string
        :param today_datetime: Date, datetime
        :param reset_hour: Boolean to start today datetime to 0:00:00
        :return:
            - events: List of events from calendar
        """

        if reset_hour:
            today_datetime = today_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

        # Define the start time (timeMin)
        today_datetime_utc = today_datetime.astimezone(pytz.utc)

        today_day = '-'.join([str(today_datetime_utc.year),
                              str(today_datetime_utc.month),
                              str(today_datetime_utc.day)])
        today_hour = ':'.join([str(today_datetime_utc.hour),
                               str(today_datetime_utc.minute),
                               '00'])  # Always 0 second

        time_min = today_day + 'T' + today_hour + 'Z'

        # Define the end time (timeMax)
        tomorrow_datetime = today_datetime
        tomorrow_datetime = tomorrow_datetime.replace(hour=23, minute=59, second=59)
        tomorrow_datetime_utc = tomorrow_datetime.astimezone(pytz.utc)

        end_day = '-'.join([str(tomorrow_datetime_utc.year),
                            str(tomorrow_datetime_utc.month),
                            str(tomorrow_datetime_utc.day)])
        end_hour = ':'.join([str(tomorrow_datetime_utc.hour),
                             str(tomorrow_datetime_utc.minute),
                             str(tomorrow_datetime_utc.second)])

        time_max = end_day + 'T' + end_hour + 'Z'

        x = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
        events = self.google_service.events().list(calendarId=calendar_id,
                                                   timeMin=time_min,
                                                   timeMax=time_max,
                                                   timeZone=x).execute()
        return events

    def get_event(self, calendar_id, event_id):
        """
        Get event in specified calendar
        :param calendar_id: ID of the calendar
        :param event_id: ID of the Event
        :return:
            - event: google calendar event
        """

        event = self.google_service.events().get(calendarId=calendar_id, eventId=event_id).execute()

        return event

    def add_event(self, event, calendar_id):
        """
        Insert event in specified calendar
        :param event: Event to add to the calendar, dict
        :param calendar_id: ID of the calendar
        :return:
            - inserted_event: google calendar event
        """

        # Change accesses to Google Calendar API in order to write events
        self.set_credentials(token_file=TOKEN_EVENTS_JSON_FILE, scopes=SCOPES_EVENTS)
        self.build_google_service_access()

        # Write event
        inserted_event = self.google_service.events().insert(calendarId=calendar_id, body=event).execute()

        # Put back the default access to Google Calendar API
        self.init_calendar_service()

        logger.info('Event added to the calendar (event: %s | calendar-id: %s)', event, calendar_id)

        return inserted_event

    def delete_event(self, google_event, calendar_id):
        """
        Delete event in specified calendar
        :param google_event: Event to delete to the calendar, google event
        :param calendar_id: ID of the calendar
        """

        # Change accesses to Google Calendar API in order to write events
        self.set_credentials(token_file=TOKEN_EVENTS_JSON_FILE, scopes=SCOPES_EVENTS)
        self.build_google_service_access()

        # Delete event
        self.google_service.events().delete(calendarId=calendar_id, eventId=google_event['id']).execute()

        # Put back the default access to Google Calendar API
        self.init_calendar_service()

        logger.info('Event deleted to the calendar (event: %s | calendar-id: %s)', google_event, calendar_id)

    def update_event(self, google_event, calendar_id):
        """
        Update event in specified calendar
        :param google_event: Event to update to the calendar, google event
        :param calendar_id: ID of the calendar
        """

        # Change accesses to Google Calendar API in order to write events
        self.set_credentials(token_file=TOKEN_EVENTS_JSON_FILE, scopes=SCOPES_EVENTS)
        self.build_google_service_access()

        # Update event
        self.google_service.events().update(calendarId=calendar_id,
                                            eventId=google_event['id'],
                                            body=google_event).execute()

        # Put back the default access to Google Calendar API
        self.init_calendar_service()

        logger.info('Event updated to the calendar (event: %s | calendar-id: %s)', google_event, calendar_id)
