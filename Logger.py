import logging


# Create a custom logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')

# Define severity
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.ERROR)

# Create formatters
text_format = '%(levelname)s - (%(filename)s)%(funcName)s:line%(lineno)d - %(message)s'
c_format = logging.Formatter(text_format, datefmt='%d-%b-%y %H:%M:%S')
f_format = logging.Formatter('%(asctime)s - ' + text_format, datefmt='%d-%b-%y %H:%M:%S')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

# logger.debug('This is a debug message')  # 10
# logger.info('This is an info message')  # 20
# logger.warning('This is a warning message')  # 30
# logger.error('This is an error message')  # 40
# logger.critical('This is a critical message')  # 50