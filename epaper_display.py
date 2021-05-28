from waveshare_epd import epd2in13
from screens import Screen2in13
import logging
from time import sleep

logger = logging.getLogger("radioAlarmLogger")

class EPaper:

    def __init__(self):
        self.epd = epd2in13.EPD()
        self.epd.init(self.epd.lut_full_update)
        self.image = None
        self.is_full_updated = True
        self.hour = 0
        self.minute = 0

    def update(self, one_datetime, event_today, event_tomorrow, notifications, force_update=False):
        """
        Update the e-paper (following the datetime)
        There is a partial update at each minute
        There is a full update at each hour

        :param one_datetime: datetime (to check if update is needed), datetime
        :param event_today: today event to display, Calendar event
        :param event_tomorrow: tomorrow event to display, Calendar event
        :param is_wifi_on: True if wifi is connected (for wifi-icon display)
        :param is_alarm_on: True if alarm is scheduled (for bell-icon display)
        :param force_update: True to force a full update of the screen
        """

        if self.need_new_screen(one_datetime, force_update):
            logger.debug('Update of the screen needed')
            self.minute = one_datetime.minute

            # Select screen mode (full or partial)
            if self.need_full_update(one_datetime, force_update):
                self.hour = one_datetime.hour
                self.set_full_update()
            else:
                self.set_partial_update()

            # Display new screen
            self.set_new_screen(one_datetime, event_today, event_tomorrow, notifications)

            if self.is_full_updated is True:
                sleep(5)
            # self.sleep()

    def need_full_update(self, one_datetime, force_update=False):
        """
        Check if a full update of the screen is needed

        :param one_datetime: datetime to check, datetime
        :param force_update: True to force a full update of the screen
        :return:
            - Boolean
        """

        if one_datetime.hour > self.hour or (one_datetime.hour == 0 and self.hour == 23) or force_update == True:
            return True
        else:
            return False

    def need_new_screen(self, one_datetime, force_update=False):
        """
        Check if a new display of the screen is needed

        :param one_datetime: datetime to check, datetime
        :param force_update: True to force a full update of the screen
        :return:
            - Boolean
        """

        if one_datetime.minute > self.minute or (one_datetime.minute == 0 and self.minute == 59) or force_update == True:
            return True
        else:
            return False

    def set_full_update(self):
        """
        Set new display update as a full update
        """
        logger.debug('Full update of e-paper')
        self.epd.init(self.epd.lut_full_update)
        self.is_full_updated = True

    def set_partial_update(self):
        """
        Set new display update as a partial update
        """
        logger.debug('Partial update of e-paper')
        self.epd.init(self.epd.lut_partial_update)
        self.is_full_updated = False

    def set_new_screen(self, one_datetime, event_today, event_tomorrow, notifications):
        """
        Define the new screen to display

        :param one_datetime: datetime to display, datetime
        :param event_today: today event to display, Calendar event
        :param event_tomorrow: tomorrow event to display, Calendar event
        :param is_wifi_on: True if wifi is connected (for wifi-icon display)
        :param is_alarm_on: True if alarm is scheduled (for bell-icon display)
        """
        current_screen = Screen2in13((self.epd.height, self.epd.width))
        current_screen.set_params(one_datetime, event_today, event_tomorrow, notifications)
        my_screen = current_screen.get_screen()
        self.epd.display(self.epd.getbuffer(my_screen))

    def sleep(self):
        """
        Put the e-paper in sleep mode
        """
        logger.info('E-paper sleep')
        self.epd.sleep()

