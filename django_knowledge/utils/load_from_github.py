import io
import zipfile
import os.path

import firebase_admin
import requests
from firebase_admin import credentials, firestore


def download_from_github_archive(owner, repo, directory):
    response = requests.get('https://github.com/{}/{}/archive/refs/heads/main.zip'.format(owner, repo))
    archive = io.BytesIO(response.content)
    with zipfile.ZipFile(archive) as archive_object:
        for member_name in archive_object.namelist():
            if not member_name.startswith('{}-main/{}/'.format(repo, directory)):
                continue

            member_info = archive_object.getinfo(member_name)
            if not member_info.is_dir():
                with archive_object.open(member_info) as member_file:
                    file_name, _ = os.path.splitext(os.path.basename(member_name))
                    file_content = str(member_file.read(), 'utf-8')
                    yield file_name, file_content


def download_from_github_directory(owner, repo, directory, token):
    graphql = """query getStartAndEndPoints {{
  repository(owner: "{}", name: "{}") {{
    object(expression: "HEAD:{}") {{
      ... on Tree {{
        entries {{
          name
          object {{
            ... on Blob {{
              text
            }}
          }}
        }}
      }}
    }}
  }}
}}""".format(owner, repo, directory)
    response = requests.post('https://api.github.com/graphql', json={'query': graphql}, headers={
        'Content-Type': 'application/json',
        'Authorization': 'bearer {}'.format(token),
        'User-Agent': 'test',
    })
    content = response.json()
    errors = content.get('errors')
    if errors:
        for error in errors:
            print(error['message'])

    data = content.get('data')
    if data:
        files = data['repository']['object']['entries']
        for file in files:
            file_name = file['name']
            file_name, _ = os.path.splitext(file_name)
            file_content = file['object']['text']
            yield file_name, file_content


class UploaderFirestore:
    MAX_PORTION_SIZE = 500

    def __init__(self, certificate):
        cred = credentials.Certificate(certificate)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.batch = self.db.batch()
        self.portion_size = 0

    def upload(self, file_name, file_content):
        ref = self.db.collection('knowledge').document(file_name)
        self.batch.set(ref, {'text': file_content})
        self.portion_size += 1

        if self.portion_size == self.MAX_PORTION_SIZE:
            self.batch.commit()

    def commit(self):
        self.batch.commit()


def run_initiator(downloader, args_downloader, uploader, args_uploader):
    downloader = globals()['download_from_{}'.format(downloader)]
    uploader = globals()['Uploader{}'.format(uploader.title())](*args_uploader)
    for file_name, file_content in downloader(*args_downloader):
        uploader.upload(file_name, file_content)

    uploader.commit()


if __name__ == '__main__':
    GITHUB_OWNER = 'TVP-Support'
    GITHUB_REPO = 'knowledge'
    GITHUB_DIRECTORY = 'db'
    GITHUB_TOKEN = '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'
    FIRESTORE_CERTIFICATE = 'knowledge.json'
    DOWNLOADER = 'github_archive'
    UPLOADER = 'firestore'

    args_downloader = {
        'github_archive': (GITHUB_OWNER, GITHUB_REPO, GITHUB_DIRECTORY),
        'github_directory': (GITHUB_OWNER, GITHUB_REPO, GITHUB_DIRECTORY, GITHUB_TOKEN),
    }
    args_uploader = {
        'firestore': (FIRESTORE_CERTIFICATE,)
    }
    run_initiator(DOWNLOADER, args_downloader[DOWNLOADER], UPLOADER, args_uploader[UPLOADER])
