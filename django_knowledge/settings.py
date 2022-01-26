import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, '../.env'))

ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'django_knowledge.urls'

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

SECRET_KEY = os.getenv('SECRET_KEY', 'j^)*90mk@i&-3$9p)0-g^!+m3)fdx^08moesscx=8=8jqr%&g0')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# KNOWLEDGE

GITHUB_OWNER = os.getenv('GITHUB_OWNER', 'TVP-Support')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'knowledge')
GITHUB_DIRECTORY = os.getenv('GITHUB_DIRECTORY', 'db')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', 'your_token')

FIRESTORE_CERTIFICATE = os.getenv('FIRESTORE_CERTIFICATE', 'knowledge.json')

TYPESENSE_SERVER = os.getenv('TYPESENSE_SERVER', 'localhost')
TYPESENSE_PORT = int(os.getenv('TYPESENSE_PORT', '8108'))
TYPESENSE_PROTOCOL = os.getenv('TYPESENSE_PROTOCOL', 'http')
TYPESENSE_API_KEY = os.getenv('TYPESENSE_API_KEY', 'your_any_key')

DEFAULT_DOWNLOADER = os.getenv('DEFAULT_DOWNLOADER', 'github_archive')
DEFAULT_UPLOADER = os.getenv('DEFAULT_UPLOADER', 'typesense')
