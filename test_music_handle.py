import time
from music_handle import *


my_radio = Radio()

def setup_function():
    my_radio.set_radio_url('nrj')

def test_turn_on_off():
    assert my_radio.on is False

    my_radio.turn_on()
    assert my_radio.on is True

    time.sleep(2)
    my_radio.turn_off()
    assert my_radio.on is False

def test_turn_on_off_internet_down():
    assert my_radio.on is False

    my_radio.turn_on(is_internet_ok=False)
    assert my_radio.on is True

    time.sleep(2)
    my_radio.turn_off()
    assert my_radio.on is False

def test_set_radio_url():
    my_radio.set_radio_url('fun')

    assert my_radio.radio == 'fun'

def test_set_radio_url_wrong():
    my_radio.set_radio_url('url_non_connu')

    assert my_radio.radio == 'nrj'
