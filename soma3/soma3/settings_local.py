from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': urqaDbConfig.get_config('DB_NAME'),
        'USER': urqaDbConfig.get_config('DB_USER'),
        'PASSWORD': urqaDbConfig.get_config('DB_PASSWORD'),
        'HOST': urqaDbConfig.get_config('DB_HOST'),
        'PORT': urqaDbConfig.get_config('DB_PORT'),
    }
}
