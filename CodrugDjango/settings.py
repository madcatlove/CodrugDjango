# -*- coding: utf-8 -*-
"""
Django settings for CodrugDjango project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys

reload(sys)
sys.setdefaultencoding('utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


#123
##### 실제 서버에 반영?
isProduction = False


#### 이미지 업로드 디렉토리.
if isProduction :
    uploadDir = '/home/codrug/upload/'
else:
    uploadDir = BASE_DIR + '/upload/'



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%cvxpxlmwv=8#yn))(84wm6cgk5ox520-2emcws06i96_5qe+@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (isProduction == False)
TEMPLATE_DEBUG = (isProduction == False)

TEMPLATE_DIRS = ( BASE_DIR + '/templates', )

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bleach',
    'CodrugWWW',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'CodrugDjango.urls'

WSGI_APPLICATION = 'CodrugDjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if isProduction == False:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'fishdiablo.net',
            'NAME': 'madcatExternal',
            'USER': 'madcatExternal',
            'PASSWORD': '1234',
            'PORT': '3306',
            'CHARSET' : 'UTF-8'
        }
    }
else :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'localhost',
            'NAME': 'codrug',
            'USER': 'codrug',
            'PASSWORD': 'codrug1234',
            'PORT': '3306',
            'CHARSET' : 'UTF-8'
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATICFILES_DIRS = (
    BASE_DIR + '/static/',
)
STATIC_URL = '/static/'


################################
# DJANGO BLEACH
# Which HTML tags are allowed
BLEACH_ALLOWED_TAGS = ['br', 'p', 'b', 'i', 'u', 'em', 'strong', 'a', 'img', 'embed', 'iframe']

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'style', 'src', 'width', 'height']

# Which CSS properties are allowed in 'style' attributes (assuming
# style is an allowed attribute)
BLEACH_ALLOWED_STYLES = [
    'font-family', 'font-weight', 'text-decoration', 'font-variant']

# Strip unknown tags if True, replace with HTML escaped characters if
# False
BLEACH_STRIP_TAGS = False

# Strip comments, or leave them in.
BLEACH_STRIP_COMMENTS = False

