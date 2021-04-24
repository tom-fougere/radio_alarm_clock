from gpio_button import *
import sys
import signal

value = 0

def print_pressed(channel):
    global value
    print('Button pressed!', value)
    value +=1


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def test_button():
    my_button = Button(gpio_pin=21)

    my_button.set_action(print_pressed)

if __name__ == '__main__':
    my_button = Button(gpio_pin=21)
    my_button.set_action(print_pressed)
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

