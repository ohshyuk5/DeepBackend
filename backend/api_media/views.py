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
from ..wsgi import db, bucket
from ..background import main

# Own
# from ~ imort ~UL

DEFAULT_BYTES = 262144


# Download
# blob = bucket.get_blob('remote/path/to/file.txt')
# print( blob.download_as_string())

# # Upload
# blob2 = bucket.blob('remote/path/storage.txt')
# blob2.upload_from_filename(filename='/local/path.txt')


class Resume(models.Model):
    pdf = models.FileField(upload_to='pdfs')
    photos = models.ImageField(upload_to='photos')


class MediaView(APIView):
    """
    POST media/
    Body: uid, rid, src, dst, result

    Request synthesizing service with two videos
    """
    def post(self, request):

        raw_data = request.body.decode('utf-8')
        data = json.loads(raw_data)

        self.uid = data['uid']
        
        # Pick random # for rid
        rid = secrets.token_hex(15)
        
        # Check for duplicated rid in the DB
        docs = db.collection(u'users').document(self.uid).collection(u'rid').stream()
        
        doc_list = []

        for doc in docs:
            doc_list.append(doc.id)

        while rid in doc_list:
            rid = secrets.token_hex(15)
        
        self.rid = str(rid)
        # self.rid = data['rid']
        self.src = data['src']
        self.dst = data['dst']

        self.result = data['result']

        # Get src & dst files
        try:
            path_src = self.get_file(self.src)    # For Firebase storage
            path_dst = self.get_file(self.dst)    # For Firebase storage
        except:
            return Response({"status":"Failed reading files from the storage"}, status=status.HTTP_404_NOT_FOUND)
        # path_src = 'backend/storage/'+ self.rid + '/src/src.mp4'    # For direct upload
        # path_dst = 'backend/storage/'+ self.rid + '/dst/dst.mp4'    # For direct upload

        # path_result = 'backend/storage/' + self.rid + '/result/'
        # if not os.path.isdir(path_result):
        #     os.mkdir(path_result)
        
        
        db_ptr = db.collection(u'users').document(self.uid).collection(u'rid').document(self.rid)
        db_ptr.set({
            'status': 'ongoing'
        })

        # os.system('nohup python ~/Server/DeepBackend/backend/background.py -u ' + self.uid + ' -r ' + self.rid + ' -s ' + path_src + ' -d ' + path_dst + ' -o ' + path_result + ' -n ' + self.result + ' &')
        
        return Response({"status":"Success", "rid":self.rid}, status=200)


    """
    GET /media
    params: uid, rid, type, name

    Get result with (user_id,req_id) pair
    """
    def get(self, request):
        try:
            uid = str(request.GET.get('uid'))
            rid = str(request.GET.get('rid'))
            typ = str(request.GET.get('type'))
            name = str(request.GET.get('name'))
            filename = name + '.mp4'

            self.result = None
            
            path = "~/Server/DeepBackend/"
            path_remote = 'users/' + uid + '/' + name + '/' + typ + '/' + filename
            path_local = 'backend/storage/temp/' + filename
            print("remote: ", path_remote)
            print("local : ", path_local)
            if not os.path.isdir('backend/storage/temp/'):
                os.mkdir('backend/storage/temp/')
            
            
            if typ != 'result':
                json_data = {
                    'status': 'Only results are accessible'
                }
                return Response(json_data, status=status.HTTP_400_BAD_REQUEST)
            
            
            # download file
            blob = bucket.get_blob(path_remote)
            # txt = blob.download_as_string()
            with open(path_local, "wb") as file_obj:
                blob.download_to_file(file_obj)
        
        # try:
        #     pass
        except:
            json_data = {
                'status': 'Cannot find file with the given name'
            }
            if path_local is not None and os.path.isfile(path_local):
                os.remove(path_local)
            return Response(json_data, status=status.HTTP_404_NOT_FOUND)
        
        

        try:
            file = FileWrapper(open(path_local, 'rb'))
            # FilePointer = open(path_local, "r")
            response = HttpResponse(file, content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename=' + filename
            if os.path.isfile(path_local):
                os.remove(path_local)
            return response

        except:
            if os.path.isfile(path_local):
                os.remove(path_local)
            json_response = {
                "status": "Cannot send file to client",
            }
            return Response(json_response, status=status.HTTP_409_CONFLICT)


    """
    Delete /media/{user_id}/{req_id}       # Delete all media sent
    """
    # def delete(self, request):
    #     try:
    #         raw_data = request.body.decode('utf-8')
    #         data = json.loads(raw_data)

    #         uid = data['uid']
    #         rid = data['rid']
    #         request = data['request']
    #         filename = data['filename']

    #         path_remote = 'users/' + uid + '/' + rid + '/' + request + '/' + filename
    #         blob = bucket.blob(path_remote)
    #         blob.delete()
    #     except:
    #         return Response({"status":"Cannot delete"}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({"status":"Deleted"}, status=200)


    def get_file(self, filename):
        if self.src == filename:
            name = "src"
        else:
            name = "dst"
        uid = self.uid
        rid = self.rid
        result = self.result

        path_remote = 'users/' + uid + '/' + result + '/' + name + '/' + filename
        path_local = 'backend/storage/' + rid + '/' + name + '/' + name + '.mp4'
        
        if not os.path.isdir('backend/storage/' + rid + '/'):
            os.mkdir('backend/storage/' + rid + '/')
        if not os.path.isdir('backend/storage/' + rid + '/' + name + '/'):
            os.mkdir('backend/storage/' + rid + '/' + name + '/')
 
        # download file
        blob = bucket.get_blob(path_remote)
        with open(path_local, "wb") as file_obj:
            blob.download_to_file(file_obj)
        return path_local
