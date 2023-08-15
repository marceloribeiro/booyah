import configparser
import os
from pathlib import Path
from string import Template
from datetime import datetime

CONFIG_FILE = 'config.ini'
INFO = 0
DEBUG = 1
WARN = 2
ERROR = 3
FATAL = 4
NAMES = ['INFO', 'DEBUG', 'WARN', 'ERROR', 'FATAL']

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
      'log_level': DEBUG,
      'log_format': '$datetime $levelname $message'
    }
    config.read(CONFIG_FILE)
    self._log_file_path = Template(config['DEFAULT']['log_file_path']).substitute(environment=ENV)
    self.log_level = int(config['DEFAULT']['log_level'])
    self.log_format = config['DEFAULT']['log_format']
  
  def can_write(self, level):
    """
    Check if log level param can be written with current log level
    """
    if self.log_level == INFO:
      return level in [ INFO, WARN, ERROR, FATAL ]
    elif self.log_level == DEBUG:
      return True
    elif self.log_level == WARN:
      return level in [ WARN, ERROR, FATAL ]
    elif self.log_level == ERROR:
      return level in [ ERROR, FATAL ]
    elif self.log_level == FATAL:
      return level == FATAL
    else:
      return False
  
  def format(self, content):
    current_datetime = datetime.now()
    return Template(self.log_format).substitute(
      message=content,
      datetime=current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    )

  def write(self, level, content):
    """
    Writes a log if allowed by level
    """
    if not self.can_write(int(level)):
      return
    
    os.makedirs(os.path.dirname(self._log_file_path), exist_ok=True)
    formatted_log_message = self.format(content)
    print(formatted_log_message)
    with open(self._log_file_path, 'a+') as f:
      f.write(formatted_log_message + "\n")
  
  def info(self, content):
    self.write(INFO, content)

  def debug(self, content):
    self.write(DEBUG, content)

  def warn(self, content):
    self.write(WARN, content)

  def error(self, content):
    self.write(ERROR, content)

  def fatal(self, content):
    self.write(FATAL, content)