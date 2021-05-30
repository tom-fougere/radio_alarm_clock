from shutil import copyfile
import logging


logger = logging.getLogger("radioAlarmLogger")
ORIGINAL_LOGGING_FILE = 'logging_files/logging_file.log'


class LoggingFileHandler:
    def __init__(self):
        self.copied = False

    def archive(self, current_time, current_logging_file=ORIGINAL_LOGGING_FILE, clear_content=True):
        """
        Archive (copy) logging file every month
        :param current_time: the current datetime, datetime
        :param current_logging_file: path of the file containing the logging message
        :param clear_content: clear content of the file containing the logging message
        """

        # Copy file when day of the month is 1 and time is 5h
        if current_time.day == 1 and current_time.hour == 5 and self.copied is False:
            logging.info('Archive logging file: {}'. format(current_logging_file))

            # split the file to get the name of the file only
            subtext = current_logging_file.split('/')

            # Build name of the file with the correct year/month
            year = current_time.year if current_time.month > 1 else current_time.year - 1
            month = (((current_time.month - 2) % 12) + 1)
            archive_logging_file = 'logging_files/{}_{:02d}_{}'.format(year, month, subtext[-1])

            # Save and copy file
            copyfile(current_logging_file, archive_logging_file)

            # Clear content of the current logging file
            if clear_content is True:
                open(current_logging_file, 'w').close()

            # Copying done
            self.copied = True

        else:
            self.copied = False

    def clear(self):
        self.copied = False
