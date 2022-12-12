import os

from dotenv import dotenv_values
config = dotenv_values('.env')
print(config.get('NAME'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.get('NAME'),
        'USER': config.get('USER'),
        'PASSWORD': config.get('PASSWORD'),
        'HOST': config.get('HOST'),
        'PORT': int(config.get('PORT')),
        'OPTIONS': {
           'options': '-c search_path=public,content'
        }
    }
}