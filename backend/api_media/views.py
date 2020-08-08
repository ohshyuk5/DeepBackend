from django.shortcuts import render
from django.db import models
from django.http import FileResponse
from django.http import HttpResponse

# rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from wsgiref.util import FileWrapper
from google.cloud import storage
import numpy as np
import json
import os
import sys
import subprocess

from ..wsgi import db, bucket

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
    POST /media/     # Request syn service with photo and video also with user_id -> req_id returned
    """
    def post(self, request):
        try:
            raw_data = request.body.decode('utf-8')
            data = json.loads(raw_data)

            self.uid = data['uid']
            self.rid = data['rid']
            self.src = data['src']
            self.dst = data['dst']
            self.result = data['result']

            path_src = self.get_file(self.src)
            path_dst = self.get_file(self.dst)
            path_result = 'backend/storage/result/'
        # try:
        #     pass
        except:
            return Response({"status":"Failed reading files from the storage"}, status=status.HTTP_404_NOT_FOUND)
        
        path = "~/Server/DeepBackend/"
        
        path_src_abs = path + path_src
        path_dst_abs = path + path_dst
        path_result_abs = path + path_result

        path_src_ext = 'backend/storage/ext/src'
        path_dst_ext = 'backend/storage/ext/dst'

        path_src_ext_abs = path + 'backend/storage/ext/src'
        path_dst_ext_abs = path + 'backend/storage/ext/dst'

        path_faceswap = path + 'backend/faceswap/faceswap.py'

        path_model_abs = path + 'backend/models/' + self.result + '/'
        print("forking")
        pid  = os.fork()

        if pid == 0:
            sys.exit(0)
            
        os.waitpid(pid, 0)
        # Extract face
        # python faceswap.py extract -i ~/faceswap/src/trump -o ~/faceswap/faces/trump
        try:
            subprocess.run(['python ' + path_faceswap + ' extract -i ' + path_src_abs + ' -o ' + path_src_ext_abs], shell=True)
            subprocess.rub(['python ' + path_faceswap + ' extract -i ' + path_dst_abs + ' -o ' + path_dst_ext_abs], shell=True)
            # os.system('python ' + path_faceswap + ' extract -i ' + path_src_abs + ' -o ' + path_src_ext_abs)
            # os.system('python ' + path_faceswap + ' extract -i ' + path_dst_abs + ' -o ' + path_dst_ext_abs)
        except:
            # TODO
            return Response({"status":"Extracting Failed"}, status=status.HTTP_400_BAD_REQUEST)

        # Train
        # python faceswap.py train -A ~/faceswap/faces/trump -B ~/faceswap/faces/cage -m ~/faceswap/trump_cage_model/
        try:
            os.system('python ' + path_faceswap + ' train -A ' + path_src_ext_abs + ' -B ' + path_dst_ext_abs + ' -m ' + path_model_abs)
        except:
            # TODO
            return Response({"status":"Training Failed"}, status=status.HTTP_400_BAD_REQUEST)


        # Convert
        # python faceswap.py convert -i ~/faceswap/src/trump/ -o ~/faceswap/converted/ -m ~/faceswap/trump_cage_model/
        try:
            os.system('python ' + path_faceswap + ' convert -i ' + path_src_abs + ' -o ' + path_result_abs + ' -m ' + path_model_abs)
        except:
            # TODO
            return Response({"status":"Converting Failed"}, status=status.HTTP_400_BAD_REQUEST)


        # Delete local files
        if path_src is not None and os.path.isfile(path_src):
                os.remove(path_src)
        if path_dst is not None and os.path.isfile(path_dst):
                os.remove(path_dst)
        # if path_src_ext is not None and os.path.isfile(path_src):
        #         os.remove(path_src)
        # if path_dst_ext is not None and os.path.isfile(path_dst):
        #         os.remove(path_dst)
        
        return Response({"status":"Success"}, status=200)


    """
    GET /media
    GET /media/{user_id}/{req_id}    # Get result with (user_id,req_id) pair
    """
    def get(self, request):
        # name = request.GET.get('name')
        # print(name)
        try:
            uid = str(request.GET.get('uid'))
            rid = str(request.GET.get('rid'))
            req = str(request.GET.get('request'))

            filename = str(request.GET.get('filename'))

            path_remote = 'users/' + uid + '/' + rid + '/' + req + '/' + filename
            path_local = 'backend/storage/' + req + '/' + filename
            
            # download file
            blob = bucket.get_blob(path_remote)
            # txt = blob.download_as_string()
            with open(path_local, "wb") as file_obj:
                blob.download_to_file(file_obj)

        except:
            json_data = {
                'status': 'Cannot find file with the given name'
            }
            if path_local is not None and os.path.isfile(path_local):
                os.remove(path_local)
            return Response(json_data, status=status.HTTP_404_NOT_FOUND)
        
        if req != 'result':
            json_data = {
                'status': 'Only results are accessible'
            }
            return Response(json_data, status=status.HTTP_400_BAD_REQUEST)

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
    def delete(self, request):
        try:
            raw_data = request.body.decode('utf-8')
            data = json.loads(raw_data)

            uid = data['uid']
            rid = data['rid']
            request = data['request']
            filename = data['filename']

            path_remote = 'users/' + uid + '/' + rid + '/' + request + '/' + filename
            blob = bucket.blob(path_remote)
            blob.delete()
        except:
            return Response({"status":"Cannot delete"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status":"Deleted"}, status=200)


    def get_file(self, filename):
        if self.src == filename:
            name = "src/"
        else:
            name = "dst/"
        
        uid = self.uid
        rid = self.rid

        try:
            path_remote = 'users/' + uid + '/' + rid + '/' + name + filename
            path_local = 'backend/storage/' + name + filename
            
            # download file
            blob = bucket.get_blob(path_remote)
            with open(path_local, "wb") as file_obj:
                blob.download_to_file(file_obj)
            return path_local

        except:
            if path_local is not None and os.path.isfile(path_local):
                os.remove(path_local)
            return None

