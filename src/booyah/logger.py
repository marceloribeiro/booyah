import logging
import os
from pathlib import Path
from string import Template

LOG_LEVEL = os.getenv('LOG_LEVEL')
LOG_FILE_PATH = os.getenv('LOG_FILE_PATH')
ENV = os.getenv('BOOYAH_ENV')

class Logger:
    """
    Used to handle server logs by levels
    You can config LOG_LEVEL and LOG_FILE_PATH in .env file
    """

    def find_parent_dir(self, start_directory, target_name):
        current_directory = os.path.abspath(start_directory)

        while current_directory != os.path.dirname(current_directory):
            if os.path.basename(current_directory) == target_name:
                return current_directory
            current_directory = os.path.dirname(current_directory)

        return None

    def __init__(self):
        base_path = os.path.dirname(self.find_parent_dir(__file__, 'src'))
        log_file_path = Template(LOG_FILE_PATH).substitute(environment=ENV, root=base_path)

        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        logging.basicConfig(
            level=LOG_LEVEL,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file_path, mode='a+'),logging.StreamHandler()]
        )

    def format(self, args, delimiter=' ', color=None, bold=False):
        if color:
            return self.colorize_message(delimiter.join([str(arg) for arg in args]), color, bold)
        return delimiter.join([str(arg) for arg in args])

    def info(self, *args, delimiter=' ', color=None, bold=False):
        logging.info(self.format(args, delimiter, color, bold))

    def debug(self, *args, delimiter=' ', color=None, bold=False):
        logging.debug(self.format(args, delimiter, color, bold))

    def warn(self, *args, delimiter=' ', color='orange', bold=False):
        logging.warning(self.format(args, delimiter, color, bold))

    def error(self, *args, delimiter=' ', color='red', bold=False):
        logging.error(self.format(args, delimiter, color, bold))

    def fatal(self, *args, delimiter=' ', color='red', bold=False):
        logging.critical(self.format(args, delimiter, color, bold))

    def colorize_message(self, message, color_name, bold=False):
        colors = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m',
            'reset': '\033[0m',
            'bold': '\033[1m'
        }

        if color_name.lower() == 'orange':
            color_code = colors['red'] + colors['yellow']
        else:
            color_code = colors.get(color_name.lower(), '')

        if bold:
            color_name += ',bold'

        color_codes = [colors.get(name, '') for name in color_name.split(',')]
        reset_code = colors['reset']
        return f"{''.join(color_codes)}{message}{reset_code}"

logger = Logger()