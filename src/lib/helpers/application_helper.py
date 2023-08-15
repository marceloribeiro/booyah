def to_camel_case(input_string):
    words = input_string.split('_')
    capitalized = []

    for word in words:
        capitalized.append(word.capitalize())

    return ''.join(capitalized)