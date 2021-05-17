from gpio_button import *
import time
import RPi.GPIO as GPIO

value = 0
GPIO_PIN = 5

def setup_function():
    global value
    value = 0

def increment_1():
    global value
    value +=1

def increment_5():
    global value
    value += 5

def test_button_short_press():
    my_button = Button(gpio_pin=GPIO_PIN)
    my_button.set_action(increment_1, increment_5)

    GPIO.setup(GPIO_PIN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    time.sleep(0.1)

    assert value == 1

def test_button_long_press():
    my_button = Button(gpio_pin=GPIO_PIN, hold_time=1)
    my_button.set_action(increment_1, increment_5)

    GPIO.setup(GPIO_PIN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(0.9)
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    time.sleep(0.1)

    assert value == 1

    GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(1.1)
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    time.sleep(0.1)

    assert value == 6

def test_button_long_press_change_hold_time():
    my_button = Button(gpio_pin=GPIO_PIN, hold_time=2)
    my_button.set_action(increment_1, increment_5)

    GPIO.setup(GPIO_PIN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(1.9)
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    time.sleep(0.1)

    assert value == 1

    GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(2.1)
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    time.sleep(0.1)

    assert value == 6

def test_button_long_press_no_function():
    my_button = Button(gpio_pin=GPIO_PIN, hold_time=1)
    my_button.set_action(increment_1)

    GPIO.setup(GPIO_PIN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(1.1)
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    time.sleep(0.1)

    assert value == 1


