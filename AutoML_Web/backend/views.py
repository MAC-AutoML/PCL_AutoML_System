from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import JSONParser

from rest_framework.authtoken.models import Token

import sys
import json
from collections import Iterable
import copy

from _app import models

from . import mock
from .parser import Parser,errParser
# Create your views here.

# class Test(APIView):
    #     def get(self, request):
    #         a = request.GET['a']
    # a,b=request.POST['username'],request.POST['password']
    # print("POST: ",request.data)
    # print(request)
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
        return Response()

        # status={
        #     "status":"ok",
        #     "type":"account",
        #     "currentAuthority":"admin",
        # }

        # return Response(data=Parser(status))
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        print(username,password)
        ### Dev mock user   
        message = '请检查填写的内容！'
        index=-1
        for (i,item) in enumerate(mock.USER_LIST):
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
            UID = mock.USER_LIST[index]['id']
            DUser = models.User.objects.filter(api_id = UID)
            if len(DUser) == 0:
                new_user = models.User.objects.create_user(
                    username=mock.USER_LIST[index]['username'],
                    tocken = mock.USER_LIST[index]['tocken'],
                    password=mock.USER_LIST[index]['password'],
                    first_name = mock.USER_LIST[index]['first_name'],
                    api_id = mock.USER_LIST[index]['id'])
                ## 不能直接把api传来的id赋值给数据库里的id，会有莫名的bug
                new_user.save()
            else:
                # DUser[0].username = username
                # DUser[0].set_password(password)
                # DUser[0].first_name = username
                DUser[0].tocken = mock.get_tocken()
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
class CurrentUser(APIView):
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
    parser_classes = (JSONParser,)
    def get(self, request):
        """
        get AutoML's record table
        """
        # 这里假设每条记录是字典形式，query结果是列表
        # [{},{},{}]
        result=mock.FAKE_Automl
        params=request.query_params.dict()
        ## 针对性解码
        params['current']=int(params['current'])
        params['pageSize']=int(params['pageSize'])
        params['sorter']=json.loads(params['sorter'])
        params['filter']=json.loads(params['filter'])
        # for (k,v)in params.items():
        #     params[k]=json.loads(v)
        print(params)
        # # 开始筛选 - key= 'type' 的类型
        selector=copy.deepcopy(params)
        # # 把传来的其他键值删掉，只保留选择用的键值对
        del(selector['current'])
        del(selector['pageSize'])
        del(selector['sorter'])
        del(selector['filter'])
        print(selector)
        # 需要一个配置文件，记录该条数据结构的键值对，对于选择形的参数，要列出其所有选项
        temp=[]
        for item in result:
            ## type: 筛选条件不在记录的类型中时,直接置为[True]
            ## 这里前端输入的可能是不完全的键,视为子串
            if(all([k=='type'and not v in mock.m_type or \
                    item[k] == v or v in item[k] \
                    for (k,v) in selector.items()])):
                temp.append(item)
        result=temp

        # selector.pop[]
        if(params['type'] in mock.m_type):
            temp=[]
            for item in result:
                if(item['type']==params['type']):
                    temp.append(item)
            result=temp
        # # filter:key
        if(len(params['filter'])):# filter 长度不为零
            temp=[]
            for item in result:
                # # 如果某个[filter]内容是[None]等不可迭代的对象,该位置直接置为[True]
                # # 如果可迭代,且 item[k]在内容 v 中,则该位置置为[True],否则置为[False]
                # # 只要存在一个[False],就说明过滤条件有不符合的,所以采用 all
                if(all([not isinstance(v,Iterable) or \
                        k=='type'and not v in mock.m_type or \
                        item[k] in v \
                        for (k,v) in params['filter'].items()])):
                    temp.append(item)
            result=temp
        response=Parser(result)
        ## 未设置则antd-pro使用 data 的长度
        # 参考网址：https://procomponents.ant.design/components/table#request
        # response['total']
        return Response(data=response)
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
