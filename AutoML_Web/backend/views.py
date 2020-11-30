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
import tools.API_tools as API_tools
from  tools.API_tools import get_keyword
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
        # 登陆用 数据接口 :
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
        '''
        for (i,item) in enumerate(mock.USER_LIST):
            if(username==item['username'] and password==item['password']):
                index=i'''
        uinfo = API_tools.check_user(username, password)
        '''
                if(index<0):
                    message = "用户名或密码错误！"
                    print(message)
                    status={"status":"error","type":"account","currentAuthority":"guest"}
                    return Response(data=status)'''
        if "错误" in uinfo:
            message = "用户名或密码错误！"
            print(message)
            status = {"status": "error", "type": "account", "currentAuthority": "guest"}
            return Response(data=status)
        else:
            UID = int(uinfo["payload"]["userInfo"]["userId"])
            DUser = models.User.objects.filter(id=UID)
            print("UID,len",UID, DUser)
            if len(DUser) == 0:
                new_user = models.User.objects.create_user(username=username,
                                                           tocken=API_tools.get_tocken(username, password),
                                                           password=password, first_name=password, id=UID)
                new_user.save()
            else:
                DUser[0].username = username
                DUser[0].set_password(password)
                DUser[0].first_name = password
                DUser[0].tocken = API_tools.get_tocken(username, password)
                DUser[0].save()
            user = auth.authenticate(
                username=username, password=password)  # 验证是否存在用户
            print(user)
            if (user):
                print("login!!!!!!!!!!!!!!!!!!")
                auth.login(request, user)
                print(request.session)
        
        response={"status":"ok", "type":"account", "currentAuthority":"user",}       
        return Response(data=response)
    def delete(self,request):
        auth.logout(request)
        return Response()
class CurrentUser(APIView):
    def get(self,request):
        user=auth.get_user(request)
        if(user.is_authenticated):
            access='user'
            return Response(data={
                "name" : str(user),
                "access":access,
            })
        return Response(data=errParser(401),status=status.HTTP_401_UNAUTHORIZED)
        # 重点是参数 status 即HTTP状态码
    def post(self, request):
        """
        post
        currentUser 只有get方法
        """
        print("Post currentUser: ",request)
        pass
from .serializers import *
class AutoML(APIView):
    # 规定解析器接受数据的格式为json
    parser_classes = (JSONParser,)

    def get(self, request):
        """
        get AutoML's record table
        """
        # 这里假设每条记录是字典形式，query结果是列表
        # [{},{},{}]
        rec = []
        queryset = models.User_Job.objects.all()
        ret = JobsSerializers(queryset, many=True)
        print("%ret%","%ret%",type(ret.data),type(ret.data[0]))
        for onejob in ret.data:
            tALG = models.User_algorithm.objects.filter(id = onejob["algorithm_id"])[0]

            rec.append(
                {
                    'id': onejob["jobid"],
                    'title': onejob["name"],
                    'type': tALG.task,
                    'train_status': onejob["state"],
                    'deploy_status': tALG.name,
                    'data_source': onejob["_path"],
                    'created_at': onejob["createdTime"],
                }
            )
        result=rec
        ## 将回传的get url参数解码成字典
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
        # # 把传来的其他键值删掉，只保留回传的筛选栏键值对
        del(selector['current'])
        del(selector['pageSize'])
        del(selector['sorter'])
        del(selector['filter'])
        print(selector)
        # 需要一个配置文件，记录不同表格每条数据 - 数据结构的键值对，对于选择形的参数，要列出其所有选项
        
        # # 处理页面上方的筛选栏回传的参数
        temp=[]
        for item in result:
            ## type: 筛选条件不在记录的类型中时,直接置为[True]
            ## 这里前端输入的可能是不完全的键,视为子串
            if(all([k=='type'and not v in mock.m_type or \
                    item[k] == v or v in item[k] \
                    for (k,v) in selector.items()])):
                temp.append(item)
        result=temp

        # if(params['type'] in mock.m_type):
        #     temp=[]
        #     for item in result:
        #         if(item['type']==params['type']):
        #             temp.append(item)
        #     result=temp
        # # filter:key 对数据进行筛选,功能与筛选栏类似
        if(len(params['filter'])):
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
            
        # # sorter: 对数据进行排序 【待完成】 
        # # 这里需要对返回给前端的所有数据进行排序
        if(len(params['sorter'])):
            pass        
        
        # # 给数据添加antd-pro推荐的传输头
        response=Parser(result)
        ## response['total'] 未设置则antd-pro使用 data 的长度
        # 参考网址：https://procomponents.ant.design/components/table#request

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
