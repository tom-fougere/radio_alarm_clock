from epaper_display import *

from datetime import datetime, timedelta

display_test = EPaper()

def test_need_full_update():
    now = datetime.now()
    display_test.datetime = now

    one_datetime = now + timedelta(minutes=59)
    assert display_test.need_full_update(one_datetime) == False

    one_datetime = now + timedelta(minutes=60)
    assert display_test.need_full_update(one_datetime) == True


def test_need_new_screen():
    now = datetime.now()
    display_test.datetime = now

    one_datetime = now + timedelta(seconds=59)
    assert display_test.need_new_screen(one_datetime) == False

    one_datetime = now + timedelta(seconds=60)
    assert display_test.need_new_screen(one_datetime) == True

    one_datetime = now + timedelta(minutes=1)
    assert display_test.need_new_screen(one_datetime) == True


if __name__ == '__main__':
    test_need_full_update()
    test_need_new_screen()

