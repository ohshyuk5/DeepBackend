from django.shortcuts import render

# rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Own
# from ~ imort ~

class MediaView(APIView):
    """
    POST /media/     # Request syn service with photo and video also with user_id -> req_id returned
    """
    def post(self, request):
        
        return Response("test post ok", status=200)

    """
    GET /media
    GET /media/{user_id}/{req_id}    # Get result with (user_id,req_id) pair
    """
    def get(self, request, **kwargs):
        if kwargs.get('user_id') is None or kwargs.get('req_id') is None:
            return Response("Invalid request", status=400)
        else:
            return Response("ok", status=200)
        
    """
    Delete /media/{user_id}/{req_id}       # Delete all media sent
    """
    def delete(self, request):
        return Response("test delete ok", status=200)