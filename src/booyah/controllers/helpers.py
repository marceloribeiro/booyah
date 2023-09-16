from booyah.controllers.application_controller import BooyahApplicationController

def before_action(block):
    BooyahApplicationController.add_before_action(block)

def after_action(block):
    BooyahApplicationController.add_after_action(block)

def around_action(block):
    BooyahApplicationController.add_around_action(block)