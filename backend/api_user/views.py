from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import numpy as np
import secrets
import json


from .serializers import UserSerializer
from .models import User
from ..wsgi import db
 
class UserView(APIView):
    """
    GET /users
    params: uid, rid

    Check whether the process finished or not
    """
    def get(self, request, **kwargs):
        # Read uid from req
        uid = request.GET.get('uid')
        print("uid: ", uid)
        if uid == None:
            return Response({'status': 'No uid'})
        else:
            uid = str(uid)
        # Read rid from req
        rid = request.GET.get('rid')
        print("rid: ", rid)
        if rid == None:
            return Response({'status': 'No rid'}, status=404)
        else:
            rid = str(rid)
        
        db_ptr = db.collection(u'users').document(uid).collection(u'rid').document(rid)
        doc = db_ptr.get()

        return Response(doc.to_dict(), status=200)
