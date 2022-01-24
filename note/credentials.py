from django.conf import settings

args_downloader = {
    'github_archive': (
        settings.GITHUB_OWNER,
        settings.GITHUB_REPO,
        settings.GITHUB_DIRECTORY,
    ),
    'github_directory': (
        settings.GITHUB_OWNER,
        settings.GITHUB_REPO,
        settings.GITHUB_DIRECTORY,
        settings.GITHUB_TOKEN,
    ),
}
args_uploader = {
    'firestore': (
        settings.FIRESTORE_CERTIFICATE,
    ),
    'typesense': (
        settings.TYPESENSE_SERVER,
        settings.TYPESENSE_PORT,
        settings.TYPESENSE_PROTOCOL,
        settings.TYPESENSE_API_KEY,
    ),
}
