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
    You can config log_level and log_file_path in configuration file
    """

    def find_parent_dir(self, start_directory, target_name):
        current_directory = os.path.abspath(start_directory)

        while current_directory != os.path.dirname(current_directory):
            if os.path.basename(current_directory) == target_name:
                return current_directory
            current_directory = os.path.dirname(current_directory)
        
        return None
    
    def __init__(self):
        base_path = os.path.dirname(self.find_parent_dir(Path.cwd(), 'src'))
        log_file_path = Template(LOG_FILE_PATH).substitute(environment=ENV, root=base_path)

        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        logging.basicConfig(
            level=LOG_LEVEL,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file_path, mode='a+'),logging.StreamHandler()]
        )

    def format(self, args, delimiter=' '):
        return delimiter.join([str(arg) for arg in args])
    
    def info(self, *args, delimiter=' '):
        logging.info(self.format(args, delimiter))

    def debug(self, *args, delimiter=' '):
        logging.debug(self.format(args, delimiter))

    def warn(self, *args, delimiter=' '):
        logging.warning(self.format(args, delimiter))

    def error(self, *args, delimiter=' '):
        logging.error(self.format(args, delimiter))

    def fatal(self, *args, delimiter=' '):
        logging.critical(self.format(args, delimiter))

logger = Logger()