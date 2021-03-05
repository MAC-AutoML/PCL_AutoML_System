from django.shortcuts import render
from django.contrib import auth
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect

from rest_framework import serializers
from rest_framework import response
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
from .serializers import *
import time
from tools.API_tools import get_keyword

# import tools.API_tools as API_tools
# from  tools.API_tools import get_keyword
sys.path.append('..')
from tools import API_tools
from .back_untils import *

## 方便debug用, VScode pylance 可以解析到这些包的位置
## 不影响正常运行
if(__name__=="__main__"):
    from ..tools import API_tools
    from .._app  import models
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
        uinfo = API_tools.check_user(username, password)
        if "错误" in uinfo:
            message = "用户名或密码错误！"
            print(message)
            response = {"status": "error", "type": "account", "currentAuthority": "guest"}
            return Response(data=response)
        else:
            UID = int(uinfo["payload"]["userInfo"]["userId"])
            DUser = models.User.objects.filter(id=UID)
            print("UID,len",UID, DUser)
            #mntpath = str(username)+"_mnt",
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

class AutoML(APIView):
    # 规定解析器接受数据的格式为json
    parser_classes = (JSONParser,)
    # @login_required
    def get(self, request):
        user=auth.get_user(request)
        # print(user)
        # print(type(user))
        # if(isinstance(user,Iterable)):
        #     for item in user:
        #         print(item)
        """
        get AutoML's record table
        """
        # 这里假设每条记录是字典形式，query结果是列表
        # [{},{},{}]
        rec = []
        updata_jobtable(user.tocken, user, user.first_name)
        queryset = models.User_Job.objects.all()
        print(queryset)
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

        if(not len(result)):
            response=Parser(result)
            return Response(data=response)            
        ## 将回传的get url参数解码成字典
        params=request.query_params.dict()
        ## 针对性解码
        params['current']=int(params['current'])
        params['pageSize']=int(params['pageSize'])
        params['sorter']=json.loads(params['sorter'])
        params['filter']=json.loads(params['filter'])
        # for (k,v)in params.items():
        #     params[k]=json.loads(v)
        # print(params)
        # # 开始筛选 - key= 'type' 的类型
        selector=copy.deepcopy(params)
        # # 把传来的其他键值删掉，只保留回传的筛选栏键值对
        del(selector['current'])
        del(selector['pageSize'])
        del(selector['sorter'])
        del(selector['filter'])
        # print(selector)
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
        # AutoML 新建任务
        # res 字典数据格式详见 @/Frontend/src/pages/AutoML/CreateMission/data.d.ts
            # export interface Former {
            # //Base set
            # type:string;
            # name:string;
            # description?:string;
            # //Dataset set
            # dataName?:string; //新建数据集的名称
            # dataOutput?:string; //新建数据集的输出路径
            # dataInput?:string; //新建数据集的输入路径
            # dataSelection?:string; // 已有数据集的id
            # //Model set
            # modelsize:number;
            # }
        # @指项目文件夹路径
        user = auth.get_user(request)

        form_dict=request.data
        # 创建任务
        print(form_dict)
        #{'type': 'Image_Classification', 'name': 'dsad', 'modelsize': 12321, 'dataSelection': 3}
        datasetname = None
        algtype = form_dict["type"]
        jobname = form_dict['name']
        maxflops = int(form_dict['modelsize'])
        datasetid = form_dict['dataSelection']
        if form_dict['dataSelection'] != None:
            datasetname = models.Dataset.objects.filter(id = int(datasetid))[0]
            print(datasetname.name)
        if algtype == 'Image_Classification':
            algdict = ["efficientnet_b3a","mobilenetv2_120d","efficientnet_lite0","mobilenetv2_100","mobilenetv3_large_100"]
            if maxflops > 900:
                algname = 'efficientnet_b3a'
            elif maxflops > 600:
                algname = 'mobilenetv2_120d'
            elif maxflops > 400:
                algname = 'efficientnet_lite0'
            elif maxflops > 300:
                algname = 'mobilenetv2_100'
            else:
                algname = 'mobilenetv3_large_100'
            #-------挂载CP算法操作----------
            #alg_cp(r'./../../algorithm/classification/pytorch_automodel/image_classification',"")

            #-----------------------------
            #command = "cd ../userhome/fakejobspace/algorithm/classification/pytorch_automodel/image_classification/;"
            command = "cd ../userhome;mkdir jobspace;cd jobspace;rm -r algorithm;mkdir algorithm;cd algorithm;" \
                      "git clone https://github.com/MAC-AutoML/PCL_AutoML_System.git;cd ..;" \
                      "mkdir image_classification;cd ..;"
            # 测试时使用fakejobspace中的算法运行
            command = command+"cd jobspace/algorithm/PCL_AutoML_System/algorithm/classification/pytorch_automodel/image_classification;"
            command = command + "PYTHONPATH=./ python Timm.py "
            expdirname = str(jobname) + "_" + str(datasetname) + "_" + str(maxflops) + "_exp_" + str(time.time())
            outputdir = "/userhome/jobspace/image_classification/"+expdirname
            command = command + " --outputdir " + outputdir
            command = command + " --dataset " + str(datasetname)
            command = command + " --algname " + str(algname)
            print(command)

            info = API_tools.creat_mission(str(jobname), command, user.tocken, user, user.first_name)
            if not info["payload"]:
                print("error~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return Response(data=errParser(errcode=404))
            timeArray = time.localtime()
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jobid = get_keyword(str(info["payload"]["jobId"]))
            name = get_keyword(str(jobname))
            username = get_keyword(str(user.username))
            user_id = str(user.id)
            state = "WAITTING"
            createdTime = get_keyword(str(otherStyleTime))
            completedTime = str(0)
            _path = get_keyword(str(outputdir))
            Da = models.User_algorithm.objects.filter(user_id=user.id).filter(name=algname)[0]
            algorithm_id = Da.id
            dataset_id = form_dict['dataSelection']
            with connection.cursor() as cursor:
                sqltext = "INSERT INTO `automl_web`.`_app_user_job`(`jobid`, `name`, `username`, `user_id`, `state`, `createdTime`, `completedTime`,`_path`, `algorithm_id`, `dataset_id`) " \
                          "VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}','{9}');".format(
                    jobid, name, username, user_id, state, createdTime, completedTime, _path, algorithm_id, dataset_id
                )
                print("$$$$$$$$$$$", sqltext)
                cursor.execute(sqltext)


        # 创建完成
        # 【】前端 后端 需要添加判断任务是否创建成功
        res=[]
        res=Parser(res)
        return Response(data=res)
        # return Response(data=errParser(errcode=404))

    def delete(self,request):
        # AutoML 删除任务
        pass

class RefreshData(APIView):
    ''' 
        更新数据集下拉列表
    '''
    def get(self,request):

        # print(request.data)
        params=request.query_params.dict()
        # 这里应该是任务类型
        typer=params["type"]
        # typer=request.query_params.dict()["type"]
        
        # 按request传来的任务类型返回需要的数据集列表
        datasets=models.Dataset.objects.filter(task=typer).all()
        ''' get dataset list '''
        if(not len(datasets)):
            return Response(data=[])
        # print(type(datasets))
        
        res=[]
        for item in datasets:
            res.append({
                'label':item.name,
                'value':item.id,
                })
        # 获取数据集列表后回传
        # 这里返回的数据集列表结构为
        # [{'label': ,'value': ,},{}]
        # res=Parser(res) # 不一定打包
        return Response(data=res)
class RefreshPath(APIView):
    def get(self,request):
        # print("Get")
        params=request.query_params.dict()
        print("Params is:",params)
        res=[]
        
        return Response(data=res)
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
        #公开算法数据库内容[{}{}{}]
        
        params=request.query_params.dict()
        print(params)
        
        rec = []
        queryset = models.Algorithm.objects.all()
        
        # if(not len(queryset)):# 返回伪造数据
        if(True):# 返回伪造数据
            result=mock.genAlgoList()
            # result=mock.ALGORITHM_LIST
        else:
        # Algo={
            #     'id' ,
            #     'name' ,
            #     'task' ,
            #     'path',
            #     'created_at',
            #     'uid',}
            ret = AlgorithmSerializers(queryset, many=True) # 
            print("%ret%", "%ret%", type(ret.data), type(ret.data[0]))
            for onejob in ret.data:

                rec.append(
                    {
                        'id':onejob["id"],
                        'name':onejob["name"],
                        'task':onejob["task"],
                        "path":onejob["_path"],
                    }
                )
            result = rec
        
        # 对get回传的筛选/搜索参数进行处理
        
        # 开始搜索
        
        # 开始筛选
        for item in result:
            ids=item['uid']
            del item['uid']
            # 这里应该从数据库里query 创建者的名字
            item['createUser']=mock.USER_LIST[ids]
        # result=result
        result=Parser(result)
        return Response(data=result)

    def post(self,request):
        form_dict=request.data
        print(form_dict)
        # 回传的筛选条件 - 字典形式
        # name type dataRange createUser
        
        result=mock.genAlgoList()
        # result=mock.ALGORITHM_LIST

        if(not len(form_dict)): # 此时说明重置，返回所有已查询
            pass
        else: # 进行条件过滤
            pass
        for item in result:
            ids=item['uid']
            del item['uid']
            # 这里应该从数据库里query 创建者的名字
            item['createUser']=mock.USER_LIST[ids]        
        result=Parser(result)
        return Response(data=result)
 
class UserAlgorithm(APIView):
    def get(self, request):
        """
        login get
        """
        #公开算法数据库内容[{}{}{}]
        rec = []
        queryset = models.User_algorithm.objects.all()
        ret = UAlgorithmSerializers(queryset, many=True)
        print("%ret%", "%ret%", type(ret.data), type(ret.data[0]))
        for onejob in ret.data:

            rec.append(
                {
                    'id':onejob["id"],
                    'name':onejob["name"],
                    'task':onejob["task"],
                    "_path":onejob["_path"],
                }
            )
        result = rec
        pass
    def post(self,request):
        pass

class PubDataset(APIView):
    def get(self, request):
        """
        login get
        """
        #公开算法数据库内容[{}{}{}]
        rec = []
        queryset = models.Dataset.objects.all()
        ret = DatasetSerializers(queryset, many=True)
        print("%ret%", "%ret%", type(ret.data), type(ret.data[0]))
        for onejob in ret.data:

            rec.append(
                {
                    'id':onejob["id"],
                    'name':onejob["name"],
                    'task':onejob["task"],
                    "_path":onejob["_path"],
                }
            )
        result = rec
        pass
    def post(self,request):
        pass


