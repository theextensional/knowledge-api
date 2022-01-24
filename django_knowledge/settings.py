import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

SECRET_KEY = os.getenv('SECRET_KEY')

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
