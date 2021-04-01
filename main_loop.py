from datetime import timedelta

from AlarmCalendar import *
from dateTime import ReliableDate
from documents.rw_dict import *


myCalendar = AlarmCalendar()
myDatetime = ReliableDate()
my_calendars = read_dict_file('documents/my_calendars.txt')

if __name__ == '__main__':

    # Init state
    myCalendar.set_calendars(alarm_calendar=my_calendars['Reveil'],
                             public_holiday_calendar=my_calendars['Jours Feries'],
                             personal_calendar=my_calendars['Elise et Tom'])

    while True:
        # Get the current datetime
        myDatetime.update()
        current_datetime = myDatetime.get_datetime()
        print(myDatetime.get_datetime_string())

        # Search if alarm is
        is_alarm_today, event_today = myCalendar.is_alarm_today(current_datetime, reset_hour=True)
        is_alarm_tomorrow, event_tomorrow = myCalendar.is_alarm_tomorrow(current_datetime)

        # Display datetime in the screen
        # display(current_datetime)
        


