import os


def comma_to_string(env_name, default=''):
    value = str(os.environ.get(env_name) or default)

    list_str = [string.strip() for string in value.split(',') if string]

    return list_str
