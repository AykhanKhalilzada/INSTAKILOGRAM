from random import sample
from string import ascii_letters, digits

MAX_TEXT_LENGTH = 128
MAX_USERNAME_LENGTH = 32
SITE_NAME = 'Instakilogram'


# main/models
def create_slug():
    template = ascii_letters + digits
    slug = ''.join(sample(template, 11))
    return slug

# web/templatetags/custom_filters
def is_full(full, unit, seconds) -> str:
    
    def is_plural(seconds):
        return 's' if seconds != 1 else ''
    
    return f' {unit}{is_plural(seconds)} ago' if full else unit[0]