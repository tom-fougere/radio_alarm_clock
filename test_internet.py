from InternetCheck import *


def test_internetchecker():

    internet = InternetChecker()

    assert internet.is_connected() is True
