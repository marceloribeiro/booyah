import inflection
class String(str):
    def __add__(self, other):
        if isinstance(other, str):
            return String(super().__add__(other))
        elif isinstance(other, String):
            return String(super().__add__(other))
        else:
            raise TypeError("Unsupported operand type")

def reverse(self):
    return self[::-1]

def constantize(self, parent_globals):
    if self in parent_globals:
        return parent_globals[self]
    else:
        raise NameError(f"Class '{self}' does not exist in parent_globals()")

def camelize(self, uppercase_first_letter=True):
    return String(inflection.camelize(self, uppercase_first_letter=uppercase_first_letter))

def dasherize(self):
    return String(inflection.dasherize(self))

def humanize(self):
    return String(inflection.humanize(self))

def ordinal(self):
    return String(inflection.ordinal(self))

def ordinalize(self):
    return String(inflection.ordinalize(self))

def parameterize(self, separator='-'):
    return String(inflection.parameterize(self, separator=separator))

def pluralize(self):
    return String(inflection.pluralize(self))

def singularize(self):
    return String(inflection.singularize(self))

def tableize(self):
    return String(inflection.tableize(self))

def titleize(self):
    return String(inflection.titleize(self))

def transliterate(self):
    return String(inflection.transliterate(self))

def underscore(self):
    clean_string = self.strip().replace(" ", "_")
    clean_string = inflection.underscore(clean_string)
    return String(clean_string.replace("__", "_"))

String.reverse = reverse
String.constantize = constantize

String.camelize = camelize
String.dasherize = dasherize
String.humanize = humanize
String.ordinal = ordinal
String.ordinalize = ordinalize
String.parameterize = parameterize
String.pluralize = pluralize
String.singularize = singularize
String.tableize = tableize
String.titleize = titleize
String.transliterate = transliterate
String.underscore = underscore

def classify(self):
    return String(String(self.titleize()).singularize().transliterate().replace(' ', ''))


String.classify = classify