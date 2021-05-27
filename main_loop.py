# External packages
import logging.config

# Personal packages
from AlarmCalendar import OnlineCalendar
from dateTime import ReliableDate
from documents.rw_dict import *
from alarms import Alarm
from events import should_the_bell_be_turned_on
from epaper_display import EPaper
from gpio_button import Button
from InternetCheck import InternetChecker
from music_handle import Radio

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger("radioAlarmLogger")

internetChecker = InternetChecker()
myCalendar = OnlineCalendar()
myDatetime = ReliableDate()
myDisplay = EPaper()
myAlarm = Alarm()
myRadio = Radio()

alarmButtonStop = Button(5)
alarmButtonSnooze = Button(6)
lightButtonIntensity = Button(23)

light_intensity = 0

def stop_alarm_button():
    logger.info('Button - Stop alarm !')
    myAlarm.stop_alarm()
    myRadio.turn_off()


def start_music():
    logger.info('Button - Start music !')
    myRadio.turn_on()


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

    while True:

        # Check internet connexion
        is_internet_ok = internetChecker.check_connection_once()

        # Get the current datetime
        myDatetime.update()
        current_datetime = myDatetime.get_datetime()
        print(myDatetime.get_datetime_string())

        # Search events in calendar
        alarm_today, event_today = myCalendar.is_alarm_today(current_datetime, reset_hour=True)
        alarm_tomorrow, event_tomorrow = myCalendar.is_alarm_tomorrow(current_datetime)

        # Set event
        myAlarm.set_event(alarm_today, event_today)

        # Set radio/music
        if is_internet_ok is True:
            myRadio.set_radio_url(myAlarm.radio)
        else:
            myRadio.set_radio_url('mp3')

        # Start music in case of alarm triggered
        if myAlarm.is_ringing(current_datetime) and myRadio.on is False:
            logger.info('Start radio / music !')
            myRadio.turn_on()

        # Select the bell icon following the current datetime (change to tomorrow after the alarm is passed)
        display_bell_icon = should_the_bell_be_turned_on(current_datetime, event_today,
                                                         alarm_today, alarm_tomorrow, limit_hour=14)

        # Display datetime in the screen
        myDisplay.update(current_datetime, event_today, event_tomorrow,
                         is_wifi_on=is_internet_ok, is_alarm_on=display_bell_icon)

