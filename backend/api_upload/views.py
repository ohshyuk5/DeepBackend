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
from ..NudeNet.porn_detection import classifier


class FileUploadView(APIView):
    """
    PUT upload/
    params: uid, rid, type

    Upload a file to the server directly
    """
    def put(self, request, filename, format=None):
        self.uid = str(request.GET.get('uid'))
        self.rid = str(request.GET.get('rid'))
        self.typ = str(request.GET.get('type'))
        self.name = str(request.GET.get('filename'))

        path_local = self.get_file()
        
        if classifier(path_local):   # True if the video is a Porn
            response = HttpResponse(json.dumps({"status":"Given video is a porn"}), content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
            return response
        
        return Response({'status':'File named ' + self.name + ' uploaded'}, status=200)

    def get_file(self):
        
        uid = self.uid
        rid = self.rid
        typ = self.typ
        name = self.name

        if not os.path.isdir('backend/storage/' + rid + '/'):
                os.mkdir('backend/storage/' + rid + '/')
        if not os.path.isdir('backend/storage/' + rid + '/' + typ + '/'):
                os.mkdir('backend/storage/' + rid + '/' + typ + '/')

        path_remote = 'users/' + uid + '/' + rid + '/' + typ + '/' + name
        path_local = 'backend/storage/' + rid + '/' + typ + '/' + typ + '.mp4'

        # download file
        blob = bucket.get_blob(path_remote)
        with open(path_local, "wb") as file_obj:
            blob.download_to_file(file_obj)
        return path_local