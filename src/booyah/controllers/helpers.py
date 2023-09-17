from booyah.controllers.application_controller import BooyahApplicationController

def before_action(block, only_for=None, except_for=None):
    BooyahApplicationController.add_before_action(block, only_for, except_for)

def after_action(block, only_for=None, except_for=None):
    BooyahApplicationController.add_after_action(block, only_for, except_for)

def around_action(block, only_for=None, except_for=None):
    BooyahApplicationController.add_around_action(block, only_for, except_for)

def skip_before_action(block, only_for=None, except_for=None):
    BooyahApplicationController.remove_before_action(block, only_for, except_for)

def skip_after_action(block, only_for=None, except_for=None):
    BooyahApplicationController.remove_after_action(block, only_for, except_for)

def skip_around_action(block, only_for=None, except_for=None):
    BooyahApplicationController.remove_around_action(block, only_for, except_for)