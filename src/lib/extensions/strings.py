import inflect
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

def camelize(self):
    words = self.split('_')
    words = [word[0].capitalize() + word[1:] for word in words if word]
    return String(''.join(words))

def constantize(self):
    if self in globals():
        return globals()[class_name]
    else:
        raise NameError(f"Class '{class_name}' does not exist in globals()")

def singularize(self):
    p = inflect.engine()
    p = String(p.singular_noun(self))
    return self if p == 'False' else p

def pluralize(self):
    p = inflect.engine()
    p = String(p.plural(self))
    return self if p == 'False' else p

def underscore(self):
    snake_case_name = ''
    for char in self:
        if char.isupper():
            snake_case_name += '_' + char.lower()
        else:
            snake_case_name += char
    if snake_case_name.startswith('_'):
        snake_case_name = snake_case_name[1:]
    return String(snake_case_name)

String.reverse = reverse
String.camelize = camelize
String.constantize = constantize
String.singularize = singularize
String.pluralize = pluralize
String.underscore = underscore

def classify(self):
    return String(self.camelize()).singularize()


String.classify = classify