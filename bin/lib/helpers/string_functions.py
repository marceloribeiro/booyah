def to_class_name(input_str, plural=False):
    words = input_str.split('_')

    # Filter out empty words and capitalize the first letter of each word
    words = [word[0].capitalize() + word[1:] for word in words if word]

    # Join the words to form the class name
    class_name = ''.join(words)

    # Apply pluralization rules if needed
    if plural:
        if class_name[-1] == 's':
            class_name += 'es'
        elif class_name.endswith(('x', 'z', 'sh', 'ch')):
            class_name += 'es'
        elif class_name.endswith('y'):
            class_name = class_name[:-1] + 'ies'
        else:
            class_name += 's'

    return class_name

def convert_to_snake_case(name):
    snake_case_name = ''
    for char in name:
        if char.isupper():
            snake_case_name += '_' + char.lower()
        else:
            snake_case_name += char
    if snake_case_name.startswith('_'):
        snake_case_name = snake_case_name[1:]
    return snake_case_name
