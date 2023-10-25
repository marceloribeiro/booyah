import json

def to_list(value, delimiter=','):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return value.split(delimiter)
    return []

def to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.lower()
        if value == "true" or value == "1":
            return True
        elif value == "false" or value == "0" or value == "":
            return False
    return bool(value)

def to_dict(value):
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        if value[0] == "'":
            return json.loads(value.replace("'", ""))
        return json.loads(value)
    return {}