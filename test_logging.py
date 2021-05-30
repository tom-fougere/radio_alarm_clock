from datetime import datetime
from os import remove, path
from logging_files import LoggingFileHandler

test_logging_file = 'logging_files/test_logging.log'

my_loggingfilehandler = LoggingFileHandler()


def setup_function():
    my_loggingfilehandler.clear()


def test_archive_no_save():

    current_datetime = datetime(year=2021, month=2, day=10, hour=14, minute=54)

    my_loggingfilehandler.archive(current_datetime, current_logging_file=test_logging_file, clear_content=False)

    assert path.isfile('logging_files/test_logging.log') is True
    assert path.isfile('logging_files/2021_02_test_logging.log') is False
    assert my_loggingfilehandler.copied is False


def test_archive_second_month_before_5():

    current_datetime = datetime(year=2021, month=2, day=1, hour=3, minute=54)

    my_loggingfilehandler.archive(current_datetime, current_logging_file=test_logging_file, clear_content=False)

    assert path.isfile('logging_files/test_logging.log') is True
    assert path.isfile('logging_files/2021_02_test_logging.log') is False
    assert my_loggingfilehandler.copied is False


def test_archive_second_month_after_5():
    current_datetime = datetime(year=2021, month=2, day=1, hour=5, minute=00)

    my_loggingfilehandler.archive(current_datetime, current_logging_file=test_logging_file, clear_content=False)

    assert path.isfile('logging_files/test_logging.log') is True
    assert path.isfile('logging_files/2021_01_test_logging.log') is True
    assert my_loggingfilehandler.copied is True

    my_loggingfilehandler.archive(current_datetime, current_logging_file=test_logging_file, clear_content=False)
    assert my_loggingfilehandler.copied is False

    remove('logging_files/2021_01_test_logging.log')


def test_archive_first_month_after_5():
    current_datetime = datetime(year=2021, month=1, day=1, hour=5, minute=00)

    my_loggingfilehandler.archive(current_datetime, current_logging_file=test_logging_file, clear_content=False)

    assert path.isfile('logging_files/test_logging.log') is True
    assert path.isfile('logging_files/2020_12_test_logging.log') is True
    assert my_loggingfilehandler.copied is True

    remove('logging_files/2020_12_test_logging.log')

