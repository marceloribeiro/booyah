from booyah.extensions.number import *

class TestNumberExtension():

    def test_ordinal(self):
        assert Number(1).ordinal() == 'st'
        assert Number(2).ordinal() == 'nd'
        assert Number(1002).ordinal() == 'nd'
        assert Number(1003).ordinal() == 'rd'
        assert Number(-11).ordinal() == 'th'
        assert Number(-1021).ordinal() == 'st'

    def test_ordinalize(self):
        assert Number(1).ordinalize() == '1st'
        assert Number(2).ordinalize() == '2nd'
        assert Number(1002).ordinalize() == '1002nd'
        assert Number(1003).ordinalize() == '1003rd'
        assert Number(-11).ordinalize() == '-11th'
        assert Number(-1021).ordinalize() == '-1021st'