import os

import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, ['*']),
)
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

ALLOWED_HOSTS = env('ALLOWED_HOSTS')
DEBUG = env('DEBUG')
ROOT_URLCONF = 'django_knowledge.urls'
WSGI_APPLICATION = 'django_knowledge.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_knowledge',
    'rest_framework',
    'note',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'sqlite3.db'),
    }
}

# KNOWLEDGE

GITHUB_OWNER = env('GITHUB_OWNER')
GITHUB_REPO = env('GITHUB_REPO')
GITHUB_DIRECTORY = env('GITHUB_DIRECTORY')
GITHUB_TOKEN = env('GITHUB_TOKEN')

FIRESTORE_CERTIFICATE = env('FIRESTORE_CERTIFICATE')

TYPESENSE_SERVER = env('TYPESENSE_SERVER')
TYPESENSE_PORT = int(env('TYPESENSE_PORT'))
TYPESENSE_PROTOCOL = env('TYPESENSE_PROTOCOL')
TYPESENSE_API_KEY = env('TYPESENSE_API_KEY')

DEFAULT_DOWNLOADER = env('DEFAULT_DOWNLOADER')
DEFAULT_UPLOADER = env('DEFAULT_UPLOADER')
