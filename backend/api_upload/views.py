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


import urllib

# Custom functions
from ..wsgi import db, bucket


class FileUploadView(APIView):
    """
    PUT upload/
    params: uid, rid, type

    Upload a file to the server directly
    """
    def post(self, request):

        # self.uid = str(request.GET.get('uid'))
        # self.rid = str(request.GET.get('rid'))
        # self.typ = str(request.GET.get('type'))
        # self.name = str(request.GET.get('filename'))

        raw_data = request.body.decode('utf-8')
        data = json.loads(raw_data)
        self.uid = data['uid']
        self.rid = data['rid']
        self.typ = data['type']
        self.name = data['filename']
        print(self.uid, self.rid, self.typ, self.name)

        path_local = self.get_file()

        os.system('python backend/background_detect.py ' + 'backend/storage/' + self.uid + '/' + self.rid + '/' + self.typ + '/ ' + self.typ + '.mp4')
        
        try:
            with open('backend/storage/' + self.uid + '/' + self.rid + '/' + self.typ + '/out.txt', 'r') as out:
                pred = out.read()
        except:
            response = Response({"status":"Fail"}, status=400)

        if pred != "Safe":
            # file = FileWrapper(open('backend/storage/' + self.rid + '/' + self.typ +'/nsfw.jpg', 'rb'))
            # filename = 'nsfw.png'
            # response = HttpResponse(file, content_type='image/png')
            # response['Content-Disposition'] = 'attachment; filename=' + filename
            self.upload_file()
            shutil.rmtree('backend/storage/' + self.uid + '/' + self.rid + '/')
            # return response
        
        # return Response({"status":"Porn"}, status=200)
        return Response({"status":pred}, status=200)

    def get_file(self):
        
        uid = self.uid
        rid = self.rid
        typ = self.typ
        name = self.name
        if not os.path.isdir('backend/storage/' + uid + '/'):
            os.mkdir('backend/storage/' + uid + '/')
        if not os.path.isdir('backend/storage/' + uid + '/' + rid + '/'):
            os.mkdir('backend/storage/' + uid + '/' + rid + '/')
        if not os.path.isdir('backend/storage/' + uid + '/' + rid + '/' + typ + '/'):
            os.mkdir('backend/storage/' + uid + '/' + rid + '/' + typ + '/')
        path_remote = 'users/' + uid + '/' + rid + '/' + typ + '/' + name
        path_local = 'backend/storage/' + uid + '/' + rid + '/' + typ + '/' + typ + '.mp4'
        
        # download file
        blob = bucket.get_blob(path_remote)
        with open(path_local, "wb") as file_obj:
            blob.download_to_file(file_obj)
        return path_local

    def upload_file(self):
        
        path_remote = 'users/' + self.uid + '/' + self.rid + '/nsfw.jpg'

        # Upload
        blob = bucket.blob(path_remote)
        blob.upload_from_filename(filename='backend/storage/' + self.uid + '/' + self.rid + '/' + self.typ +'/nsfw.jpg')

        return