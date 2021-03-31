from AlarmCalendar import *

from datetime import timedelta

myCalendar = GoogleCalendarAPI()

if __name__ == '__main__':

    # Init state
    myCalendar.init_calendar_service()

    while():
        # Get the current datetime
        current_datetime = get_current_time()

        # Search if alarm is
        is_alarm_today, event_today = myCalendar.is_alarm_today(current_datetime)
        is_alarm_tomorrow, event_tomorrow = myCalendar.is_alarm_today(current_datetime + timedelta(days=1))

        display(current_datetime)
        


