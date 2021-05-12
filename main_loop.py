# External packages
import logging.config

# Personal packages
from AlarmCalendar import AlarmCalendar
from dateTime import ReliableDate
from documents.rw_dict import *
from events import Event
from epaper_display import EPaper
from gpio_button import Button
from InternetCheck import InternetChecker
from music_handle import Radio

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger("radioAlarmLogger")

internetChecker = InternetChecker()
myCalendar = AlarmCalendar()
myDatetime = ReliableDate()
myDisplay = EPaper()
myAlarm = Event()
myRadio = Radio()

alarmButtonStop = Button(21)
alarmButtonSnooze = Button(22)
lightButtonIntensity = Button(23)

light_intensity = 0

def stop_alarm_button(channel):
    logger.info('Button - Stop alarm !')
    myAlarm.stop_alarm()
    myRadio.turn_off()


def snooze_alarm_button(channel):
    logger.info('Button - Snooze alarm !')
    myAlarm.snooze()
    myRadio.turn_off()


def change_light_intensity(channel):
    global light_intensity
    new_intensity = divmod(light_intensity + 1, 10)
    logger.info('Button - Change light from intensity %s to %s !', light_intensity, new_intensity)


if __name__ == '__main__':

    # Init state
    my_calendars = read_dict_file('documents/my_calendars.txt')
    myCalendar.set_calendars(alarm_calendar=my_calendars['Reveil'],
                             public_holiday_calendar=my_calendars['Jours Feries'],
                             personal_calendar=my_calendars['Elise et Tom'])

    # Check internet connexion
    is_internet_ok = internetChecker.is_connected()

    # Set button action
    alarmButtonStop.set_action(stop_alarm_button)
    alarmButtonSnooze.set_action(snooze_alarm_button)
    lightButtonIntensity.set_action(change_light_intensity)

    while True:
        # Check internet connexion
        is_internet_ok = internetChecker.check_connection_once()

        # Get the current datetime
        myDatetime.update()
        current_datetime = myDatetime.get_datetime()
        print(myDatetime.get_datetime_string())

        # Search events in calendar
        is_alarm_today, event_today = myCalendar.is_alarm_today(current_datetime, reset_hour=True)
        is_alarm_tomorrow, event_tomorrow = myCalendar.is_alarm_tomorrow(current_datetime)

        # Set event
        myAlarm.set_event(is_alarm_today, event_today)
        myRadio.set_radio_url(myAlarm.radio)

        # Select the bell icon following the current datetime (change to tomorrow after the alarm is passed)
        if current_datetime <= myAlarm.end_time:
            display_bell_icon = is_alarm_today
        else:
            display_bell_icon = is_alarm_tomorrow

        # Start music in case of alarm triggered
        if myAlarm.is_ringing(current_datetime):
            logger.info('Start radio/music !')
            display_bell_icon = event_tomorrow
            myRadio.turn_on()

        # Display datetime in the screen
        myDisplay.update(current_datetime, [event_today, event_tomorrow],
                         is_wifi_on=is_internet_ok, is_alarm_on=display_bell_icon)

        


