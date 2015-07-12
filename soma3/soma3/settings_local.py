from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': urqaDbConfig.get_config('DB_NAME', 'local'),
        'USER': urqaDbConfig.get_config('DB_USER', 'local'),
        'PASSWORD': urqaDbConfig.get_config('DB_PASSWORD', 'local'),
        'HOST': urqaDbConfig.get_config('DB_HOST', 'local'),
        'PORT': urqaDbConfig.get_config('DB_PORT', 'local'),
    }
}
