from django.shortcuts import render
from django.db import models
from django.http import FileResponse
from django.http import HttpResponse

# rest_framework
from rest_framework.response import Response
from rest_framework import status

from wsgiref.util import FileWrapper
from google.cloud import storage
import numpy as np
import json
import os
import sys
import subprocess
import getopt
import shutil

if __name__ == '__main__':
    if __package__ is None:
        from os import path
        sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
        from wsgi import db, bucket
    else:
        from .wsgi import db, bucket


def main(argv):

    FILE_NAME = argv[0]

    try:
        opts, etc_args = getopt.getopt(argv[1:], "u:r:s:d:o:n:", ["help", "instance=", "channel="])

    except:
        print(FILE_NAME, '-i <instance name> -c <channel name>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == "-s":
            path_src = arg
        elif opt == "-d":
            path_dst = arg
        elif opt == "-o":
            path_result = arg
        elif opt == "-u":
            uid = arg
        elif opt == "-r":
            rid = arg
        elif opt == "-n":
            name = arg

    path = "~/Server/DeepBackend/"
        
    path_src_abs = path + path_src
    path_dst_abs = path + path_dst
    path_result_abs = path + path_result

    path_src_ext = 'backend/storage/' + rid + '/ext/src'
    path_dst_ext = 'backend/storage/' + rid + '/ext/dst'

    path_src_ext_abs = path + 'backend/storage/' + rid + '/ext/src'
    path_dst_ext_abs = path + 'backend/storage/' + rid + '/ext/dst'

    path_faceswap = path + 'backend/faceswap/faceswap.py'
    
    path_model_abs = path + 'backend/models/' + rid +'/'

    path_remote = 'users/' + uid + '/' + name + '/result/' + name + '.mp4'

    if not os.path.isdir('backend/models/' + rid +'/'):
        os.mkdir('backend/models/' + rid +'/')

    # Extract face
    # python faceswap.py extract -i ~/faceswap/src/trump -o ~/faceswap/faces/trump
    
    # os.system('python ' + path_faceswap + ' extract -i ' + path_src_abs + ' -o ' + path_src_ext_abs)
    # os.system('python ' + path_faceswap + ' extract -i ' + path_dst_abs + ' -o ' + path_dst_ext_abs)

    # Train
    # python faceswap.py train -A ~/faceswap/faces/trump -B ~/faceswap/faces/cage -m ~/faceswap/trump_cage_model/
    
    # os.system('python ' + path_faceswap + ' train -A ' + path_dst_ext_abs + ' -B ' + path_src_ext_abs + ' -m ' + path_model_abs)
    
    # Convert
    # python faceswap.py convert -i ~/faceswap/src/trump/ -o ~/faceswap/converted/ -m ~/faceswap/trump_cage_model/
    
    # os.system('python ' + path_faceswap + ' convert -i ' + path_dst_abs + ' -o ' + path_result_abs + 'imgs/' + ' -m ' + path_model_abs)
    
    # Generating a video
    # os.system('ffmpeg -f image2 -i ' + path_result_abs + 'imgs/dst_%6d.png ' + path_result_abs + 'out.mp4')


    # if path_src is not None and os.path.isfile(path_src):
    #     os.remove(path_src)
    # if path_dst is not None and os.path.isfile(path_dst):
    #     os.remove(path_dst)


    # Upload
    # blob = bucket.blob(path_remote)
    # blob.upload_from_filename(filename=path_result + 'out.mp4')

    # db_ptr = db.collection(u'users').document(uid).collection(u'rid').document(rid)
    # db_ptr.set({
    #     'status': 'done'
    # })

    shutil.rmtree('backend/storage/' + rid + '/') 
    shutil.rmtree('backend/models/' + rid + '/') 
    
if __name__ == '__main__':
    main(sys.argv)