from calendarAPI import *

OFF_STRING = 'off'
FORCE_STRING = 'force'


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
        day, month, year = today_datetime.day, today_datetime.month, today_datetime.year
        day = str(day).zfill(2)
        month = str(month).zfill(2)
        year = str(year).zfill(4)

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

        is_alarm = True if len(events_alarm_calendar['items']) > 0 else False
        is_force_alarm, force_event = get_specific_event(events_alarm_calendar, FORCE_STRING)
        is_off_event, off_event = get_specific_event(events_personal_calendar, OFF_STRING)
        is_public_holiday, public_holiday_event = get_specific_event(events_public_holiday_calendar)

        is_alarm_today = is_force_alarm or (is_alarm and (not is_off_event and not is_public_holiday))

        alarm_event = None
        if is_force_alarm:
            alarm_event = force_event
        elif is_alarm and not is_off_event:
            alarm_event = events_alarm_calendar['items'][0]
        elif is_alarm and not is_public_holiday:
            alarm_event = events_alarm_calendar['items'][0]
        elif is_off_event:
            alarm_event = off_event
        elif is_public_holiday:
            alarm_event = public_holiday_event

        return is_alarm_today, alarm_event


def get_specific_event(events, substring=''):
    is_event = False
    specific_event = None

    for event in events['items']:
        if substring in event['summary'].lower():
            is_event = True
            specific_event = event
            break

    return is_event, specific_event


if __name__ == '__main__':
    # main()
    myCalendar = AlarmCalendar()
    myCalendar.set_calendars('primary', 'primary', 'primary')
    myCalendar.is_alarm_today('')
    # print(myCalendar.get_list_calendars_name())
    # print(myCalendar.get_events_of_day('primary', '2021', '03', '24'))
