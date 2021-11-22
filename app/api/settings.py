import os
import sys
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', default='8JtSQz8eVdRmLW&P6dVN')


DOMAIN = os.getenv('DOMAIN')
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,10.0.2.2").split(",")
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', default=587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', f'contact@{DOMAIN}')
# ACTIVATION_PATH_ON_EMAIL = 'verify_email'
# PASSWORD_RESET_PATH_ON_EMAIL = 'reset_password'
# PASSWORD_SET_PATH_ON_EMAIL = 'set_password'
# EMAIL_SUBJECT_ACTIVATION = 'E-Mail verifizieren'

print('default from')
print(DEFAULT_FROM_EMAIL)

# Application definition

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'user',
  'graphene_django',
  'graphql_auth',
  'django_filters',
  'graphql_jwt.refresh_token.apps.RefreshTokenConfig'
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
  'graphql_jwt.backends.JSONWebTokenBackend',
  'django.contrib.auth.backends.ModelBackend',
  'graphql_auth.backends.GraphQLAuthBackend'
]

GRAPHQL_JWT = {
  'JWT_VERIFY_EXPIRATION': True,
  'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
  'JWT_ALLOW_ANY_CLASSES': [
    'graphql_auth.mutations.Register',
    'graphql_auth.mutations.VerifyAccount',
    'graphql_auth.mutations.ResendActivationEmail',
    'graphql_auth.mutations.SendPasswordResetEmail',
    'graphql_auth.mutations.PasswordReset',
    'graphql_auth.mutations.ObtainJSONWebToken',
    'graphql_auth.mutations.VerifyToken',
    'graphql_auth.mutations.RefreshToken',
    'graphql_auth.mutations.RevokeToken',
  ],
}

GRAPHQL_AUTH = {
    'LOGIN_ALLOWED_FIELDS': ['email'],
    'REGISTER_MUTATION_FIELDS': ['email'],
    'USER_NODE_EXCLUDE_FIELDS': ['username'],
    'USER_NODE_FILTER_FIELDS': {
        'email': ['exact'],
    }
}

GRAPHENE = {
    'SCHEMA': 'api.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

if DEBUG == 'True':
  ALLOWED_HOSTS += ['*', 'localhost', '127.0.0.1']
  # MIDDLEWARE.append('corsheaders.middleware.CorsMiddleware')
  # INSTALLED_APPS.append('corsheaders')
  #
  # CORS_ORIGIN_ALLOW_ALL = True
  # CORS_ALLOW_CREDENTIALS = True
  # CORS_ALLOW_HEADERS = ['Location', 'Set-Cookie', 'X-CSRFToken', 'x-csrftoken', 'content-type']
  # CORS_ALLOW_METHODS = [
  #   'DELETE',
  #   'GET',
  #   'OPTIONS',
  #   'PATCH',
  #   'POST',
  #   'PUT',
  # ]

AUTH_USER_MODEL = 'user.User'
ROOT_URLCONF = 'api.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'api.wsgi.application'

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if DEVELOPMENT_MODE is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/api/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
