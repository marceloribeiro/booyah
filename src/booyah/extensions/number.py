import inflection
from booyah.extensions.string import String

class Number(int):
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

def megabytes(self):
    return Number(self * 1024 * 1024)

def kilobytes(self):
    return Number(self * 1024)

Number.ordinal = ordinal
Number.ordinalize = ordinalize
Number.megabytes = megabytes
Number.kilobytes = kilobytes
