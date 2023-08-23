import inflection
import booyah.extensions.string
globals()['String'] = booyah.extensions.string.String

class Number(str):
    def __add__(self, other):
        if isinstance(other, int):
            return Number(super().__add__(other))
        elif isinstance(other, int):
            return Number(super().__add__(other))
        else:
            raise TypeError("Unsupported operand type")

def ordinal(self):
    return String(inflection.ordinal(self))

def ordinalize(self):
    return String(inflection.ordinalize(self))

Number.ordinal = ordinal
Number.ordinalize = ordinalize
