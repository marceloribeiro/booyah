def to_camel_case(input_string):
    words = input_string.split('_')
    return ''.join([word.capitalize() for word in words])