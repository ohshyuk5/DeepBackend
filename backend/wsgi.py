"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only
env_path = './.env'
load_dotenv(dotenv_path=env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()

################
# 파이어 베이스 연결
################
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

cred = credentials.Certificate(os.environ.get('FIRESTORE_KEY'))

app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'cs492-team-a.appspot.com'
})

db = firestore.client()

bucket = storage.bucket(app=app)
