from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dungeonhaven',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'GMLord',
        'PASSWORD': 'The Right to GM',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

