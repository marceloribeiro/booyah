import inspect
import os
from booyah.logger import logger
from booyah.observers.application_model_observer import ApplicationModelObserver

def caller_class():
    current_frame = inspect.currentframe()
    caller_frame = inspect.getouterframes(current_frame, 2)
    if os.getenv('BOOYAH_ENV') == 'test':
        return caller_frame[2][3]
    else:
        return caller_frame[1][3]

def before_save(*blocks):
    for block in blocks:
        ApplicationModelObserver.add_callback('before_save', caller_class(), block)

def after_save(*blocks):
    for block in blocks:
        ApplicationModelObserver.add_callback('after_save', caller_class(), block)

def before_create(*blocks):
    for block in blocks:
        ApplicationModelObserver.add_callback('before_create', caller_class(), block)

def after_create(*blocks):
    for block in blocks:
        ApplicationModelObserver.add_callback('after_create', caller_class(), block)

def before_update(*blocks):
    for block in blocks:
        ApplicationModelObserver.add_callback('before_update', caller_class(), block)

def after_update(*blocks):
    for block in blocks:
        ApplicationModelObserver.add_callback('after_update', caller_class(), block)

def before_destroy(*blocks):
    for block in blocks:
        ApplicationModelObserver.add_callback('before_destroy', caller_class(), block)

def after_destroy(*blocks):
    for block in blocks:
        ApplicationModelObserver.add_callback('after_destroy', caller_class(), block)

def before_validation(*blocks):
    for block in blocks:
        ApplicationModelObserver.add_callback('before_validation', caller_class(), block)

def after_validation(*blocks):
    for block in blocks:
        ApplicationModelObserver.add_callback('after_validation', caller_class(), block)