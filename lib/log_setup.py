import logging
import os
from logging.handlers import RotatingFileHandler
import sys

# Pi installs to /home/Piano-LED-Visualizer; elsewhere use the project root.
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_log_dir = '/home/Piano-LED-Visualizer' if os.path.isdir('/home/Piano-LED-Visualizer') else _project_root
_log_file = os.path.join(_log_dir, 'visualizer.log')

# Create a custom logger
logger = logging.getLogger("my_app")

# Set the level of this logger.
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = RotatingFileHandler(_log_file, maxBytes=500000, backupCount=10)


# Set the level for handlers
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


# Custom exception handler to log unhandled exceptions
def log_unhandled_exception(exc_type, exc_value, exc_traceback):
    logger.error("Unhandled Exception: ", exc_info=(exc_type, exc_value, exc_traceback))


# Set the custom exception handler
sys.excepthook = log_unhandled_exception
