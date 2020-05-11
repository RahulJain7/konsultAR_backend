from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, response, status, views
from django.contrib.auth import get_user_model

from app_users.models import AppUser
from . import permissions as perm
from . import serializers as app_users_serializers
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
mycol = mydb['app_users_appuser']
from bson.objectid import ObjectId
User = get_user_model()




class UserBaseView(generics.GenericAPIView):

    def get_user(self):
        return get_object_or_404(
            self.models.AppUser.objects.all(),
        )

class RegisterAppUserAPIView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        firstname = request.data['first_name']
        lastname = request.data['last_name']
        mobile = request.data['mobile']
        password = request.data['password']
        role = request.data['role']
        email_val = self.validator('email',email)
        print (email_val)
        if not email_val:
            return JsonResponse({'detail':"Email already registered"},status=400,safe=False)
        mobile_val = self.validator('mobile',mobile)
        if not mobile_val:
            return JsonResponse({'detail':"Mobile already registered"},status=400,safe=False)
        user_obj = User(
            email=email,
            mobile=mobile,
        )
        user_obj.set_password(password)
        user_obj.is_active = True
        user_obj.save()
        validated_data = {'email':email,'first_name':firstname,'last_name':lastname,'mobile':mobile,'status':'offline','role':role}
        AppUser.objects.create(user=user_obj,**validated_data)
        return JsonResponse(validated_data,safe=False)




    def validator(self,field,email):
        qs = {field:email}
        res = mycol.find_one(qs)
        print (res)
        if res:
            return False
        else:
            return True
    # queryset = AppUser.objects.all()
    # serializer_class = app_users_serializers.AppUserRegisterSerializer
    # permission_classes = [anonperm]

    # def get_serializer_context(self, *args, **kwargs):
    #     return {"request": self.request}


class LoginAppUserAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request, *args, **kwargs):
        get_user = request.user
        user_qs = User.objects.filter(id=get_user.id).first()
        qs = {'email':user_qs.email}
        app_user_qs = mycol.find_one(qs)
        ser_resp = json.loads(json_util.dumps(app_user_qs))
        return JsonResponse(ser_resp,safe=False)

class ChangeStatusAPIView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def post(self,request, *args, **kwargs):
        status = request.data['status']
        get_user = request.user
        user_qs = User.objects.filter(id=get_user.id).first()
        qs = {'email':user_qs.email}
        mycol.update_one(qs,{'$set':{'status':status}})
        return JsonResponse({"result":"success"},safe=False)

class UsersStatusAPIView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self,request, *args, **kwargs):
        usrs = mycol.find()
        exp_users = []
        for usr in usrs:
            if usr['role'] == 'expert':
                name = usr['first_name']+' '+usr['last_name']
                sts = usr['status']
                usr_dict = {"name":name,"status":sts}
                exp_users.append(usr_dict)
        return JsonResponse({'result':exp_users},safe=False)
            




class AppUserCreateView(UserBaseView):
    """
    Model View
    """
    serializer_class = app_users_serializers.AppUserRegisterSerializer

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