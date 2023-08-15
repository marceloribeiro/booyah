import logging
import configparser
import os
from pathlib import Path
from string import Template

CONFIG_FILE = 'config.ini'
DEFAULT_LOG_LEVEL = 'INFO'
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
  
  def __init__(self):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
      'log_file_path': os.path.join(Path.cwd(), 'logs', '$environment.log'),
      'log_level': DEFAULT_LOG_LEVEL,
    }

    if not os.path.exists(CONFIG_FILE):
      with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    else:
      config.read(CONFIG_FILE)
    
    self._log_file_path = Template(config['DEFAULT']['log_file_path']).substitute(environment=ENV)
    self.log_level = log_levels.get(config['DEFAULT']['log_level'], DEFAULT_LOG_LEVEL)

    os.makedirs(os.path.dirname(self._log_file_path), exist_ok=True)
    logging.basicConfig(filename=self._log_file_path, level=self.log_level, format="%(asctime)s - %(levelname)s - %(message)s")
  
  def info(self, content):
    logging.info(content)

  def debug(self, content):
    logging.debug(content)

  def warn(self, content):
    logging.warning(content)

  def error(self, content):
    logging.error(content)

  def fatal(self, content):
    logging.critical(content)