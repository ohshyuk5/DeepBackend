from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from .models import User
 
class UserView(APIView):
    """
    POST /user
    """
    def post(self, request):
        user_serializer = UserSerializer(data=request.data) #Request의 data를 UserSerializer로 변환       
        if user_serializer.is_valid():
            user_serializer.save() #UserSerializer의 유효성 검사를 한 뒤 DB에 저장
            return Response(user_serializer.data, status=status.HTTP_201_CREATED) #client에게 JSON response 전달
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    """
    GET /user
    GET /user/{user_id}
    """
    def get(self, request, **kwargs):
        # return Response("test get ok", status=200)
        if kwargs.get('user_id') is None:
            user_queryset = User.objects.all() #모든 User의 정보를 불러온다.
            user_queryset_serializer = UserSerializer(user_queryset, many=True)
            return Response(user_queryset_serializer.data, status=status.HTTP_200_OK)
        else:
            user_id = kwargs.get('user_id')
            user_serializer = UserSerializer(User.objects.get(id=user_id)) #id에 해당하는 User의 정보를 불러온다
            return Response(user_serializer.data, status=status.HTTP_200_OK)
 
    """
    PUT /user/{user_id}
    """
    def put(self, request, **kwargs):
        if kwargs.get('user_id') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            user_id = kwargs.get('user_id')
            user_object = User.objects.get(id=user_id)
 
            update_user_serializer = UserSerializer(user_object, data=request.data)
            if update_user_serializer.is_valid():
                update_user_serializer.save()
                return Response(update_user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
 
    """
    DELETE /user/{user_id}
    """
    def delete(self, request, **kwargs):
        if kwargs.get('user_id') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            user_id = kwargs.get('user_id')
            user_object = User.objects.get(id=user_id)
            user_object.delete()
            return Response("deleted", status=status.HTTP_200_OK)

