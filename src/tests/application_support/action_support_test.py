from booyah.controllers.application_controller import BooyahApplicationController
from booyah.controllers.helpers import *

class MyController(BooyahApplicationController):
    before_action('do_something')
    before_action('do_something_only', only_for=['index'])
    before_action('do_something_except', except_for=['index'])
    before_action('do_something_skipped')
    skip_before_action('do_something_skipped')
    before_action('do_something_skipped_only_for')
    skip_before_action('do_something_skipped_only_for', only_for=['show'])
    before_action('do_something_skipped_except_for')
    skip_before_action('do_something_skipped_except_for', except_for=['show'])

    def __init__(self, environment):
        super().__init__(environment)
        self.environment['HTTP_ACCEPT'] = 'text/html'
        self.before_action_called_skipped = None
        self.before_action_called_skipped_only_for = None
        self.do_something_skipped_except_for = None

    def do_something(self):
        self.before_action_called = 'true'

    def do_something_only(self):
        self.before_action_called_only = 'do_something_only'

    def do_something_except(self):
        self.before_action_called = 'do_something_except'

    def do_something_skipped(self):
        self.before_action_called_skipped = 'do_something_skipped'

    def do_something_skipped_only_for(self):
        self.before_action_called_skipped_only_for = 'do_something_skipped_only_for'

    def index(self):
        return self.respond_to(html=lambda: self.render({'message': 'Hello World'}))

class TestApplicationSupport:
    def test_before_action_handler(self):
        c = MyController({})
        c.run_action(c.get_action('index'))
        assert c.before_action_called == 'true'

    def test_before_action_only_for(self):
        c = MyController({})
        c.run_action(c.get_action('index'))
        assert c.before_action_called_only == 'do_something_only'

    def test_before_action_except_for(self):
        c = MyController({})
        c.run_action(c.get_action('index'))
        assert c.before_action_called != 'do_something_except'

    def test_skip_before_action(self):
        c = MyController({})
        c.run_action(c.get_action('index'))
        assert c.before_action_called_skipped != 'do_something_skipped'

    def test_skip_before_action_with_only_for(self):
        c = MyController({})
        c.run_action(c.get_action('index'))
        assert c.before_action_called_skipped_only_for == 'do_something_skipped_only_for'

    def test_skip_before_action_with_except_for(self):
        c = MyController({})
        c.run_action(c.get_action('index'))
        assert c.do_something_skipped_except_for != 'do_something_skipped_except_for'