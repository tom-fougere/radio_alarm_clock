import RPi.GPIO as GPIO

class Button:
    def __init__(self, gpio_pin=0):
        self.pin = gpio_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def set_action(self, function):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=function, bouncetime=300)