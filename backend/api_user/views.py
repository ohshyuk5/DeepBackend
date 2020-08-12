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
    POST /users
    유저 등록
    """
    def post(self, request):
        # user_serializer = UserSerializer(data=request.data) #Request의 data를 UserSerializer로 변환       
        # if user_serializer.is_valid():
        #     user_serializer.save() #UserSerializer의 유효성 검사를 한 뒤 DB에 저장
        #     return Response(user_serializer.data, status=status.HTTP_201_CREATED) #client에게 JSON response 전달
        # else:
        #     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            raw_data = request.body.decode('utf-8')
            data = json.loads(raw_data)
            uid = data['uid']
            
        except:
            json_data = {
                'status': 'user id error'
            }
            return Response(json_data, status=status.HTTP_400_BAD_REQUEST)
        
        ################################################
        # TODO check whether uid is already used or not
        ################################################

        json_data = {
            'uid': uid
        }
        db_ptr = db.collection(u'users').document(uid)
        db_ptr.set({
            'status': 'init'
        })

        return Response(json_data, status=status.HTTP_200_OK)
        
 
    """
    GET /users
    GET /users/{user_id}
    합성이 완료 되었는지 확인
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
    # """
    # PUT /users/{user_id}
    # """
    # def put(self, request, **kwargs):
    #     if kwargs.get('user_id') is None:
    #         return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         user_id = kwargs.get('user_id')
    #         user_object = User.objects.get(id=user_id)
 
    #         update_user_serializer = UserSerializer(user_object, data=request.data)
    #         if update_user_serializer.is_valid():
    #             update_user_serializer.save()
    #             return Response(update_user_serializer.data, status=status.HTTP_200_OK)
    #         else:
    #             return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
 
    """
    DELETE /users/{user_id}
    유저 정보 삭제
    """
    # def delete(self, request, **kwargs):
    #     if kwargs.get('user_id') is None:
    #         return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         user_id = kwargs.get('user_id')
    #         user_object = User.objects.get(id=user_id)
    #         user_object.delete()
    #         return Response("deleted", status=status.HTTP_200_OK)

