import os

WORKING_DIR = (
    '/home/audemus/mysite'
)
DOCS_CREDENTIALS = os.path.join(
    WORKING_DIR, 'secrets', 'docs_credentials.json'
)
DOCS_FLOW_TOKEN = os.path.join(
    WORKING_DIR, 'secrets', 'docs_token.pickle'
)