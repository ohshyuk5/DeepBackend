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
    def post(self, request):
        
        raw_data = request.body.decode('utf-8')
        data = json.loads(raw_data)

        uid = data['uid']
        
        # Pick random # for rid
        rid = secrets.token_hex(15)
        
        # Check for duplicated rid in the DB
        docs = db.collection(u'users').document(uid).collection(u'rid').stream()
        
        doc_list = []

        for doc in docs:
            doc_list.append(doc.id)

        while rid in doc_list:
            rid = secrets.token_hex(15)
        
        rid = str(rid)
        response = HttpResponse(json.dumps({"status":"Success", "rid":rid}), content_type='application/json', status=status.HTTP_200_OK)
        return response
        
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
        # print("1")
        if doc.to_dict() == None:
            # print("2")
            response = HttpResponse(json.dumps({"status":"No process"}), content_type='application/json', status=status.HTTP_404_NOT_FOUND)
        else:
            # print("3")
            print(doc.to_dict())
            response = HttpResponse(json.dumps(doc.to_dict()), content_type='application/json', status=status.HTTP_200_OK)

        return response
