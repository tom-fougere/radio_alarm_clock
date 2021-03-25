import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/calendar']
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

CREDENTIALS_FILE = 'credentials.json'


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
        if os.path.exists('token.json'):
            self.credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                self.credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
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



# def get_calendar_service():
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#
#     service = build('calendar', 'v3', credentials=creds)
#     return service
#
#
# def main():
#     service = get_calendar_service()
#     # Call the Calendar API
#     print('Getting list of calendars')
#     calendars_result = service.calendarList().list().execute()
#
#     calendars = calendars_result.get('items', [])
#
#     if not calendars:
#         print('No calendars found.')
#     for calendar in calendars:
#         summary = calendar['summary']
#         id = calendar['id']
#         primary = "Primary" if calendar.get('primary') else ""
#         print("%s\t%s\t%s" % (summary, id, primary))


if __name__ == '__main__':
    # main()
    myCalendar = GoogleCalendarAPI()
    myCalendar.init_calendar_service()
