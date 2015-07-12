from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': urqaDbConfig.get_config('DB_NAME'),               # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': urqaDbConfig.get_config('DB_USER'),
        'PASSWORD': urqaDbConfig.get_config('DB_PASSWORD'),
        'HOST': urqaDbConfig.get_config('DB_HOST'),                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': urqaDbConfig.get_config('DB_PORT'),                      # Set to empty string for default.
    }
}

if is_unittest():
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'ATOMIC_REQUESTS': True,
    }