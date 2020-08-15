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
    def put(self, request):
        raw_data = request.body.decode('utf-8')
        data = json.loads(raw_data)

        # self.uid = str(request.GET.get('uid'))
        # self.rid = str(request.GET.get('rid'))
        # self.typ = str(request.GET.get('type'))
        # self.name = str(request.GET.get('filename'))

        self.uid = data['uid']
        self.rid = data['rid']
        self.typ = data['type']
        self.name = data['filename']

        # path_local = self.get_file()

        url = 'http://5ba580bdaa79.ngrok.io/api/'
        data = {'path': "helo"}
        data = json.dumps(data)
        data = str(data)
        
        post_data = raw_data.encode('utf-8')
        req = urllib.request.Request(url, post_data)
        res = urllib.request.urlopen(req, timeout = 1000)
        data = json.loads(res.read())

        if data["status"] == "Safe":
            self.get_file()
        else:
            shutil.rmtree('backend/storage/' + self.rid + '/')
        
        return Response(data, status=200)
        # return Response({"status":"good"}, status=200)

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