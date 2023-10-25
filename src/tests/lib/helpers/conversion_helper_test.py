from booyah.helpers.conversion import *
class TestClass():
    pass

class TestStringExtension():
    def test_to_bool(self):
        assert to_bool(True) == True
        assert to_bool('hello') == True
        assert to_bool('True') == True
        assert to_bool('true') == True
        assert to_bool('1') == True
        assert to_bool('') == False
        assert to_bool([0]) == True
        assert to_bool({'a': '0'}) == True
        assert to_bool(False) == False
        assert to_bool('False') == False
        assert to_bool('false') == False
        assert to_bool('0') == False
        assert to_bool([]) == False
        assert to_bool({}) == False

    def test_to_list(self):
        assert to_list([1, 2]) == [1, 2]
        assert to_list('1,2') == ['1', '2']

    def test_to_dict(self):
        assert to_dict({'a': 'b', 'c': 1}) == {'a': 'b', 'c': 1}
        assert to_dict('{"a": "b", "c": 1}') == {'a': 'b', 'c': 1}
        assert to_dict('\'{"a": "b", "c": 1}\'') == {'a': 'b', 'c': 1}