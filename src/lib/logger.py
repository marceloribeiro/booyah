import logging
import configparser
import os
from pathlib import Path
from string import Template

CONFIG_FILE = 'config.ini'
DEFAULT_LOG_LEVEL = 'DEBUG'
log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

ENV = 'development'

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
        config = configparser.ConfigParser()
        base_path = os.path.dirname(self.find_parent_dir(Path.cwd(), 'src'))
        default_log_file_path = '$root/logs/$environment.log'
        config['DEFAULT'] = {
            'log_file_path': default_log_file_path,
            'log_level': DEFAULT_LOG_LEVEL,
        }

        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)
        else:
            config.read(CONFIG_FILE)
        
        self._log_file_path = Template(config['DEFAULT']['log_file_path']).substitute(environment=ENV, root=base_path)
        print(self._log_file_path)
        self.log_level = log_levels.get(config['DEFAULT']['log_level'], DEFAULT_LOG_LEVEL)

        os.makedirs(os.path.dirname(self._log_file_path), exist_ok=True)
        logging.basicConfig(
            level=self.log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(self._log_file_path, mode='a+'),logging.StreamHandler()]
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