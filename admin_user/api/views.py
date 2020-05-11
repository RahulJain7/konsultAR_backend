from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, response, status, views
from django.contrib.auth import get_user_model

from admin_user.models import AdminUser
from . import permissions as perm
from . import serializers as app_user_serializers
from django.http import JsonResponse
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
anonperm = perm.AnonPermissionOnly
from bson.json_util import dumps
import pymongo
from bson import json_util, ObjectId
from rest_framework.response import Response
import json
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['kar-db']
mycol = mydb['admin_user_adminuser']
from bson.objectid import ObjectId
User = get_user_model()




class UserBaseView(generics.GenericAPIView):

    def get_user(self):
        return get_object_or_404(
            self.models.AppUser.objects.all(),
        )

class RegisterAdminUserAPIView(generics.CreateAPIView):
    queryset = AdminUser.objects.all()
    serializer_class = app_user_serializers.AdminUserRegisterSerializer
    permission_classes = [anonperm]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}



class AdminUserCreateView(UserBaseView):
    """
    Model View
    """
    serializer_class = app_user_serializers.AdminUserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(

                # user = request.user,
                # oem=request.user.oem,
                # parent=None

            )
            return response.Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
                content_type="application/json"
            )
        return response.Response(
            data={
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST,
        )