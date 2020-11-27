from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework.authtoken.models import Token

import sys
sys.path.append("..")
from _app import models

from .mock import USER_LIST,get_tocken

from .parser import Parser,errParser
# Create your views here.

# class Test(APIView):
    #     def get(self, request):
    #         a = request.GET['a']
    #         res = {
    #             'success': True,
    #             'data': 'a'
    #         }
    #         return Response(res)
## 每个页面对应一个类?
class OverView(APIView):
    def get(self, request):
        pass
        return Response()
    def post(self,request):
        pass
    
class Login(APIView):
    def get(self, request):
        """
        login get
        """
        status={
            "status":"ok",
            "type":"account",
            "currentAuthority":"admin",
        }

        return Response(data=Parser(status))
    def post(self,request):
        # a,b=request.POST['username'],request.POST['password']
        print("POST: ",request.data)
        print(request)
        
        username = request.data['username']
        password = request.data['password']
        print(username,password)
        ### Dev mock user   
        message = '请检查填写的内容！'
        index=-1
        for (i,item) in enumerate(USER_LIST):
            name=item['username']
            pw=item['password']
            if(username==name and password==pw):
                index=i
        if(index<0):
            message = "用户名或密码错误！"
            print(message)
            status={"status":"error","type":"account","currentAuthority":"guest"}
            return Response(data=status)
        else:
            #检查并创建数据库用户
            UID = USER_LIST[index]['id']
            DUser = models.User.objects.filter(api_id = UID)
            if len(DUser) == 0:
                new_user = models.User.objects.create_user(
                    username=USER_LIST[index]['username'],
                    tocken = USER_LIST[index]['tocken'],
                    password=USER_LIST[index]['password'],
                    first_name = USER_LIST[index]['first_name'],
                    api_id = USER_LIST[index]['id'])
                ## 不能直接把api传来的id赋值给数据库里的id，会有莫名的bug
                new_user.save()
            else:
                # DUser[0].username = username
                # DUser[0].set_password(password)
                # DUser[0].first_name = username
                DUser[0].tocken = get_tocken()
                DUser[0].save()
            user = auth.authenticate(
                username=username, password=password)  # 验证是否存在用户
            print(user)
            if (user):
                print("login!!!!!!!!!!!!!!!!!!")
                auth.login(request, user)
                print(request.session)     
        
        status={"status":"ok", "type":"account", "currentAuthority":"user",}       
        return Response(data=status)
    def delete(self,request):
        auth.logout(request)
        return Response()
class currentUser(APIView):
    def get(self,request):
        user=auth.get_user(request)
        access='guest'
        if(user.is_authenticated):
            access='user'
            return Response(data={
                "name" : str(user),
                "access":access,
            })
        return Response(data={
            "data": {
            "isLogin": "false",
            },
            "errorCode": '401',
            "errorMessage": '请先登录！',
            "success": "true",
        },status=status.HTTP_401_UNAUTHORIZED)
    def post(self, request):
        """
        post
        """
        print("Post currentUser: ",request)
        pass
class AutoML(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class CreateMission(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class DataManage(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class DevEnv(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
     
class AlgoManage(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class TrainJobManage(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class AutoJobManage(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class ModelManage(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class AIMarket(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
