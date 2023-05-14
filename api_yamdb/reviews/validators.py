import re

from django.core.exceptions import ValidationError
from django.conf import settings





def regex_validator(value):
    MESSAGE_SYMBOLS = 'Некорректные символы: {}'
    invalid_simbols = ''.join(set(re.sub(r'([\w.@+-]+)', '', str(value))))
    if invalid_simbols:
        raise ValidationError(MESSAGE_SYMBOLS.format(invalid_simbols))
    return value


def reserved_names_validator(value):
    MESSAGE = 'Невозможно использовать {} в качестве имени пользователя.'
    for reserved_username in settings.RESERVED_USERNAMES:
        if value == reserved_username:
            raise ValidationError(MESSAGE.format(value))
    return value
