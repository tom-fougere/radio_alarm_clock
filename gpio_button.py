import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("radioAlarmLogger")


class Button:
    def __init__(self, gpio_pin=0, hold_time=2):
        # Init attributes
        self.pin = gpio_pin
        self.hold_time = hold_time
        self.time_press = datetime.now()
        self.time_release = self.time_press
        self.pressed = False
        self.action_done = False
        self.function_short_press = None
        self.function_long_press = None

        # Init gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def set_action(self, function_short_press, function_long_press=None):

        self.function_short_press = function_short_press
        self.function_long_press = function_long_press

        GPIO.remove_event_detect(self.pin)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.start_action, bouncetime=1)

    def start_action(self, channel=None):

        callback_function = self.function_short_press

        # PRESSED
        if not GPIO.input(self.pin):
            logger.info("Button pressed!")
            self.time_press = datetime.now()
            self.pressed = True
            self.action_done = False

        # RELEASED
        if GPIO.input(self.pin) and self.pressed is True:
            logger.info("Button released!")
            self.pressed = False
            self.time_release = datetime.now()

            # if the hold time is reached (and the function exists), set the next action as a long pressed action
            if self.function_long_press is not None and \
                            self.time_release >= (self.time_press + timedelta(seconds=self.hold_time)) and \
                            self.function_long_press is not None:
                callback_function = self.function_long_press

        # Run action
        if self.pressed is False and self.action_done is False:
            callback_function()
            self.action_done = True


