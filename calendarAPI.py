import datetime
import pytz
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

CREDENTIALS_FILE = 'documents/credentials.json'
TOKEN_JSON_FILE = 'documents/token.json'


class GoogleCalendarAPI:

    def __init__(self):
        self.credentials = None
        self.google_service = None

    def init_calendar_service(self):
        """
        Authorizing requests to the Google Calendar API
        """
        self.credentials = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TOKEN_JSON_FILE):
            self.credentials = Credentials.from_authorized_user_file(TOKEN_JSON_FILE, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                self.credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_JSON_FILE, 'w') as token:
                token.write(self.credentials.to_json())

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
