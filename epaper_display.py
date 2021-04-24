from waveshare_epd import epd2in13
from screens import Screen2in13

class EPaper:

    def __init__(self):
        self.epd = epd2in13.EPD()
        self.epd.init(self.epd.lut_full_update)
        self.image = None
        self.is_full_updated = True
        self.hour = 0
        self.minute = 0

    def update(self, one_datetime, events, is_wifi_on=False, is_alarm_on=True, force_update=False):

        # Select screen mode (full or partial)
        if self.need_full_update(one_datetime, force_update):
            self.hour = one_datetime.hour
            self.set_full_update()
        elif self.is_full_updated:
            self.set_partial_update()

        if self.need_new_screen(one_datetime, force_update):
            self.minute = one_datetime.minute

            # Display new screen
            self.set_new_screen(one_datetime, events, is_wifi_on=is_wifi_on, is_alarm_on=is_alarm_on)
            self.sleep()

    def need_full_update(self, one_datetime, force_update=False):
        if one_datetime.hour > self.hour or (one_datetime.hour == 0 and self.hour == 23) or force_update == True:
            return True
        else:
            return False

    def need_new_screen(self, one_datetime, force_update=False):
        if one_datetime.minute > self.minute or (one_datetime.minute == 0 and self.minute == 59) or force_update == True:
            return True
        else:
            return False

    def set_full_update(self):
        self.epd.init(self.epd.lut_full_update)
        self.is_full_updated = True

    def set_partial_update(self):
        self.epd.init(self.epd.lut_partial_update)
        self.is_full_updated = False

    def set_new_screen(self, one_datetime, events, is_wifi_on=False, is_alarm_on=True):
        current_screen = Screen2in13((self.epd.height, self.epd.width))
        current_screen.set_params(one_datetime, events, is_wifi_on=is_wifi_on, is_alarm_on=is_alarm_on)
        my_screen = current_screen.get_screen()
        self.epd.display(self.epd.getbuffer(my_screen))

    def sleep(self):
        print('Sleep')
        self.epd.sleep()

