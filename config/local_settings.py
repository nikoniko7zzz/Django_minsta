import os

#settings.pyからそのままコピー
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = '**************************' # settings.py から該当部分コピー
SECRET_KEY = 'django-insecure-fjj!29uml7e+w6@mx9d+g&%s_4qs(@a&b2=d3swc!gscjm2+#a'


#settings.pyからそのままコピー
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEBUG = True