# External packages
import logging.config
from datetime import datetime, timedelta
from time import sleep

# Personal packages
from AlarmCalendar import OnlineCalendar
from dateTime import ReliableDate
from documents.rw_dict import *
from alarms import Alarm
from epaper_display import EPaper
from gpio_button import Button
from InternetCheck import InternetChecker
from music_handle import Radio
from notifications import Notifications

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger("radioAlarmLogger")

internetChecker = InternetChecker()
myCalendar = OnlineCalendar()
myDatetime = ReliableDate()
myDisplay = EPaper()
myAlarm = Alarm()
myRadio = Radio()
myNotifications = Notifications()

alarmButtonStop = Button(5)
alarmButtonSnooze = Button(6)
lightButtonIntensity = Button(23)

light_intensity = 0
offset_datetime_debug = timedelta(days=3)

def stop_alarm_button():
    logger.info('Button - Stop alarm !')
    myAlarm.stop_alarm()
    myRadio.turn_off()


def start_music():
    logger.info('Button - Start music !')

    # Check internet connexion
    is_internet_ok = internetChecker.check_connection_once()

    # Turn on the music
    myRadio.turn_on(is_internet_ok=is_internet_ok)


def snooze_alarm_button():
    logger.info('Button - Snooze alarm !')
    myAlarm.snooze()
    myRadio.turn_off()


def force_alarm():
    logger.info('Button - Force alarm !')
    dt = myDatetime.get_datetime()
    myCalendar.force_alarm(dt)


def change_light_intensity():
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
    alarmButtonStop.set_action(stop_alarm_button, force_alarm)
    alarmButtonSnooze.set_action(snooze_alarm_button, start_music)
    lightButtonIntensity.set_action(change_light_intensity)

    events_today = []
    events_tomorrow = []

    myDatetime.update()
    previous_datetime = myDatetime.get_datetime() - timedelta(hours=1) - offset_datetime_debug

    while True:
        sleep(2)

        # Check internet connexion
        is_internet_ok = internetChecker.check_connection_once()

        # Get the current datetime
        myDatetime.update()
        current_datetime = myDatetime.get_datetime() - offset_datetime_debug
        print(myDatetime.get_datetime_string())

        # Update events and alarm every hour
        if current_datetime >= (previous_datetime + timedelta(hours=1)):

            # Update previous datetime
            previous_datetime = current_datetime

            # Search events in calendar
            events_today = myCalendar.get_events(current_datetime, reset_hour=True)
            events_tomorrow = myCalendar.get_events(current_datetime + timedelta(days=1), reset_hour=True)

            # Set event
            myAlarm.set_event(events_today[0])

            # Set radio/music
            myRadio.set_radio_url(myAlarm.radio)

        # Define notifications (wifi icon, alarm icon, intervention icon)
        myNotifications.set_wifi(is_internet_ok)
        myNotifications.define_calendar_intervention_notif(events_today)
        myNotifications.define_alarm_notif(current_datetime, events_today[0], events_tomorrow[0])
        notifications = myNotifications.get_values()

        # Display
        myDisplay.update(current_datetime, events_today[0], events_tomorrow[0], notifications)

        # Start music in case of alarm triggered
        if myAlarm.is_ringing(current_datetime) and myRadio.on is False:
            logger.info('Start radio / music !')
            myRadio.turn_on()


