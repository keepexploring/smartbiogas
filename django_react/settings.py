"""
Django settings for django_react project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ConfigParser
import configparser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Config = ConfigParser.ConfigParser() # we store security setting in another file
Config.read(BASE_DIR+'/config/configs.ini')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Config.get("django","secret_key")
#'frobam8*+@h(p%#8ft+)x=e73d_t(jch3hn%-nf+6f=y5zq=kb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['46.101.93.225','127.0.0.1','localhost','api.smartbiogas.org']

# LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = 'home'

MEDIA_ROOT = os.path.join(BASE_DIR, 'Images')
MEDIA_URL ='/media/'


# Application definition

INSTALLED_APPS = (
    'dal',
    'dal_select2',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_postgres_extensions',
    'webpack_loader',
    'django_dashboard',
    'django_react',
    'django_elasticsearch_dsl',
    'channels',
    'django_realtime',
    'huey.contrib.djhuey',
    'tastypie',
    'oauth2_provider',
    'corsheaders',
    'tastypie_oauth2',
    'django_seed',
    'dynamic_raw_id',
    'searchableselect',
    'datetimepicker',
    'phonenumber_field',
    'autofixture',
    #'django_seed',
)

MIDDLEWARE_CLASSES = (
    'django_react.disable.DisableCSRF',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True # this should be restricted in the future for security

#TASTYPIE_SWAGGER_API_MODULE = 'django_dashboard.urls.api'

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'},
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',

}

ROOT_URLCONF = 'django_react.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_react.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   # },
    # 'data': {
    #     'ENGINE': 'sql_server.pyodbc',
    #     'NAME': Config.get("azure", "database"),
    #     'USER': Config.get("azure", "username"),
    #     'PASSWORD': Config.get("azure", "password"),
    #     'HOST': Config.get("azure", "server"),
    #     'PORT': '',

    #     'OPTIONS': {
    #         'driver': 'ODBC Driver 13 for SQL Server',
    #     },
    
    # },
        'default': {
            #'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': Config.get("postgres_azure", "database_name"),
            'USER': Config.get("postgres_azure", "username"),
            'PASSWORD': Config.get("postgres_azure", "password"),
            'HOST': Config.get("postgres_azure", "host"),
            'PORT': Config.get("postgres_azure", "port"),

        }
}

DATABASE_CONNECTION_POOLING = True

#DATABASE_ROUTERS = ['django_dashboard.routers.Dashboard_Router',]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
#STATIC_ROOT 

STATICFILES_DIRS = (
     os.path.join(BASE_DIR, 'assets'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}


ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },
}

#OAUTH2_PROVIDER = { # add these setting for OAuth
#
#}


# In production we should use a redis backend
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'asgi_redis.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [('localhost', 6379)],
#         },
#         'ROUTING': 'example_channels.routing.channel_routing',
#     }
# }

CHANNEL_LAYERS = {
 "default": {
 "BACKEND": "asgiref.inmemory.ChannelLayer",
 "ROUTING": "django_realtime.routing.channel_routing",
 },
}


HUEY = {
    'name': 'django_huey',  # Use db name for huey.
    'result_store': True,  # Store return values of tasks.
    'events': True,  # Consumer emits events allowing real-time monitoring.
    'store_none': False,  # If a task returns None, do not save to results.
    'always_eager': False,  # If DEBUG=True, run synchronously.
    'store_errors': True,  # Store error info if task throws exception.
    'blocking': False,  # Poll the queue rather than do blocking pop.
    'connection': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'connection_pool': None,  # Definitely you should use pooling!
        # ... tons of other options, see redis-py for details.

        # huey-specific connection parameters.
        'read_timeout': 1,  # If not polling (blocking pop), use timeout.
        'max_errors': 1000,  # Only store the 1000 most recent errors.
        'url': None,  # Allow Redis config via a DSN.
    },
    'consumer': {
        'workers': 4,
        'worker_type': 'thread',
        'initial_delay': 0.1,  # Smallest polling interval, same as -d.
        'backoff': 1.15,  # Exponential backoff using this rate, -b.
        'max_delay': 10.0,  # Max possible polling interval, -m.
        'utc': True,  # Treat ETAs and schedules as UTC datetimes.
        'scheduler_interval': 1,  # Check schedule every second, -s.
        'periodic': True,  # Enable crontab feature.
        'check_worker_health': True,  # Enable worker health checks.
        'health_check_interval': 1,  # Check worker health every second.
    },
}
