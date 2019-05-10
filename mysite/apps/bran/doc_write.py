import logging
import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from apps.bran import utils

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents'
]

def get_service():
    creds = None
    if os.path.isfile(utils.DOCS_FLOW_TOKEN):
        with open(utils.DOCS_FLOW_TOKEN, 'rb') as token:
            creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    utils.DOCS_CREDENTIALS, SCOPES
                )
                creds = flow.run_local_server()
            with open(utils.DOCS_FLOW_TOKEN, 'wb') as token:
                pickle.dump(creds, token)
        return build('docs', 'v1', credentials=creds)

def filename(user, title, subtitle):
    return '{user} - {title} {subtitle}'.format(
        user=user, title=title, subtitle=subtitle
    )

def write_body(posts, users):
    requests = []
    for post, user in zip(posts, users):
        user_text = '{user}\n\n'.format(user=user)
        post_text = '{post}\n\n'.format(post=post)
        for text in [user_text, post_text]:
            requests.append({
                'insertText': {
                    'text': text,
                    'endOfSegmentLocation': {
                        'segmentId': None
                    }
                }
            })
    return requests

def write_file(filename, posts, users, service):
    doc = service.documents().create(
        body={'title': filename}
    ).execute()
    print('Created document with title: {}'.format(doc.get('title')))
    requests = write_body(posts, users)
    doc = service.documents().batchUpdate(
        documentId=doc['documentId'],
        body={'requests': requests}
    ).execute()
    return doc

def doc_url(doc):
    return (
    'https://docs.google.com/document/d/{document_id}/edit'.format(
        document_id=doc['documentId']
    ))
