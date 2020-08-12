from django.shortcuts import render
from django.db import models
from django.http import FileResponse
from django.http import HttpResponse


# rest_framework
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from wsgiref.util import FileWrapper
from google.cloud import storage
import numpy as np
import json
import os
import secrets
import sys
import subprocess
import shutil

# Custom functions
from ..wsgi import db, bucket


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]
    
    def get(self, request):

        rid = str(secrets.token_hex(15))

        return Response({'status':'Success', 'rid':rid}, status=200)

    def put(self, request, filename, format=None):
        uid = str(request.GET.get('uid'))
        rid = str(request.GET.get('rid'))
        typ = str(request.GET.get('type'))
        
        file_obj = request.data['file']
        if not os.path.isdir('backend/storage/' + rid + '/'):
                os.mkdir('backend/storage/' + rid + '/')
        if not os.path.isdir('backend/storage/' + rid + '/' + typ + '/'):
                os.mkdir('backend/storage/' + rid + '/' + typ + '/')

        with open('backend/storage/'+ rid + '/' + typ + '/' + typ + '.mp4', 'wb') as f:
            for line in file_obj:
                f.write(line)
        
        return Response({'status':'Uploaded'}, status=200)