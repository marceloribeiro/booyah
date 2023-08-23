from booyah.helpers.application_helper import *

class TestApplicationHelper():
    def test_to_camel_case(self):
      assert to_camel_case('test_string') == 'TestString'