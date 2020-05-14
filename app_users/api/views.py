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
from pyfcm import FCMNotification
from opentok import OpenTok
FCM_URL = "https://fcm.googleapis.com"
FCM_SERVER_KEY = "AAAAUJc35IM:APA91bG7TyiQ7rWgibA3ZcqlW0_giMVCxDwzigmzyhpZO-YKqgdZBnSvdFa2TNeFYaYW_0Z2xTAPQ4MFfrmjNo97awGWSeel7Q-ODz3tCZp2Ulmv3QTQsiL0tWVWwDrYBGZ2Ovv6mrtO"


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

    def post(self,request, *args, **kwargs):
        fcmid = request.data['fcmid']
        get_user = request.user
        user_qs = User.objects.filter(id=get_user.id).first()
        qs = {'email':user_qs.email}
        mycol.update_one(qs,{'$set':{'status':'online'}})
        mycol.update_one(qs,{'$set':{'fcmid':fcmid}})
        app_user_qs = mycol.find_one(qs)
        app_user_qs.pop('fcmid')
        ser_resp = json.loads(json_util.dumps(app_user_qs))
        return JsonResponse(ser_resp,safe=False)

class LogoutAppUserAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request, *args, **kwargs):
        get_user = request.user
        user_qs = User.objects.filter(id=get_user.id).first()
        qs = {'email':user_qs.email}
        mycol.update_one(qs,{'$set':{'status':'offline'}})
        return JsonResponse({"result":"Success"},safe=False)


class GetARSessionAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request, *args, **kwargs):
        opentok = OpenTok('46640082', '27254ec0aeb2fb70021007f55c9dfb26078b727d')
        session = opentok.create_session()
        session_id = session.session_id
        token = session.generate_token()
        return JsonResponse({"ar_session_id":session_id,"ar_token":token},safe=False)


class CallAnswerAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self,request, *args, **kwargs):
        answer = request.data['answer']
        tech_email = request.data['tech_email']
        session_id = request.data['session_id']
        token = request.data['token']
        tech_qs = {'email':tech_email}
        tech_res = mycol.find_one(tech_qs)
        fcm_id = tech_res['fcmid']
        message_title = "Video Call Answer"
        if answer == 'accepted':
            message_body = "Call accepted"
            message_data = {'status':'accepted','ar_session_id':session_id,'ar_token':token}
        else:
            message_body = "Call rejected"
            message_data = {"status":"rejected"}
        result = FCMNotification(api_key=FCM_SERVER_KEY).notify_single_device(registration_id=fcm_id, message_title=message_title,data_message=message_data,message_body=message_body,click_action="com.com.example.virosample_VIDEO_CALL")
        return JsonResponse({'result':'success'},safe=False)

class GetARSessionIDAPIView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self,request, *args, **kwargs):
        user = request.user
        usr = User.objects.filter(id=user.id).first()
        user_qs = {'email':usr.email}
        user_js = mycol.find_one(user_qs)
        session_id = user_js['ar_session_id']
        token = user_js['ar_token']
        return JsonResponse({"ar_session_id":session_id,"ar_token":token},safe=False)




class SendCallRequestAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request, *args, **kwargs):
        print (request.data)
        expert_user_email = request.data['expert_email']
        expert_user_qs = {'email':expert_user_email}
        expert_user= mycol.find_one(expert_user_qs)
        fcm_id = expert_user['fcmid']
        tech_user_user = request.user
        tech_user = User.objects.filter(id=tech_user_user.id).first()
        tech_user_qs = {'email':tech_user.email}
        tech_user_js = mycol.find_one(tech_user_qs)
        tech_name = tech_user_js['first_name'] + ' ' + tech_user_js['last_name']
        tech_eml = tech_user_js['email']
        message_title = "Video Call"
        message_body = "Call from " + tech_name
        message_data = {'tech_name':tech_name,'tech_email':tech_eml}
        result = FCMNotification(api_key=FCM_SERVER_KEY).notify_single_device(registration_id=fcm_id, message_title=message_title, message_body=message_body,data_message=message_data,click_action="com.com.example.virosample_VIDEO_CALL")
        return JsonResponse({"result":"Success"},safe=False)

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
                eml = usr['email']
                usr_dict = {"name":name,"status":sts,'email':eml}
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