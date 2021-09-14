"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from django.contrib import admin
from django.urls import path, include

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fjj!29uml7e+w6@mx9d+g&%s_4qs(@a&b2=d3swc!gscjm2+#a'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

# ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com']
ALLOWED_HOSTS = ['*']
# Application definition

# ユーザーログインモデルの定義
AUTH_USER_MODEL = 'register.User'

INSTALLED_APPS = [
    'django.contrib.admin',  # 自作のユーザーモデルを使うのでコメントアウト
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'register.apps.RegisterConfig',
    'study.apps.StudyConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('register.urls')),
# ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            # viewから直接自分で渡さなくてもテンプレート上で変数を使えるようにするもの
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'study.context_processors.common',  # context_processors.pyの変数を読み込む
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = 'register:login'
LOGIN_REDIRECT_URL = 'register:top'
LOGOUT_REDIRECT_URL = 'register:top'

# メールをコンソールに表示する
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if DEBUG:
    def show_toolbar(request):
        return True

    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    # ここで表示する内容を設定できます↓↓基本的にはこれでok
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }


#
# Github https: // github.com/nikoniko7zzz/Django_aione.git
# /Personals/niko/opt/anaconda3/envs/djangoenv/lib/python3.8/site-packages(21.0.1)
# pip install -r requirements.txt
# conda activate djangoenv
# conda deactivate
# python manage.py makemigrations
# python manage.py migrate


# kuucham.pythonanywhere.com
# pa_autoconfigure_django.py --python=3.8 https://github.com/nikoniko7zzz/Django_aione.git --nuke

# deactivate
# cd ~/kuucham.pythonanywhere.com
# git pull
# workon kuucham.pythonanywhere.com
# (kuucham.pythonanywhere.com)$ python manage.py collectstatic
