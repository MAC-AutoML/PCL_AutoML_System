from django.shortcuts import render
from django.contrib import auth
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from requests.models import ContentDecodingError

from rest_framework import serializers
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import JSONParser

from rest_framework.authtoken.models import Token

import os
import sys
import json
import copy
import time
import datetime
import re
import multiprocessing
from collections import Iterable

from _app import models

from . import mock
from .parser import Parser,errParser
from .serializers import *
import time

# import tools.API_tools as API_tools
# from  tools.API_tools import get_keyword
sys.path.append('..')
from tools import API_tools
from . import back_untils

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
RES_TYPE=[
    ["gpuNumber","cpuNumber","memoryMB","shmMB"],
    [0, 4,  16384,  8192],
    [1, 4,  32768,  16384],
    [1, 8,  65536,  32768],
]
METHODS=['BBO','BORE','HyperBand']
PLIST=[]
# POOL=multiprocessing.Pool(8)
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
        # print(username,password)
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
        back_untils.updata_jobtable(user.tocken, user, user.first_name)
        queryset = models.User_Job.objects.all()
        # print(queryset)
        ret = JobsSerializers(queryset, many=True)
        # print("%ret%","%ret%",type(ret.data),type(ret.data[0]))
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
        print(params)
        
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
        # 需要一个配置文件，记录不同表格每条数据 - 数据结构的键值对，在这个配置文件中，对于需要用户选择的参数，要列出其所有选项
        
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
        #{'type': 'Image_Classification', 'name': 'dsad', 'modelsize': 12321, 'dataSelection': 3}
        FRONT_DEBUG=True
        if(not FRONT_DEBUG):
            datasetname = None
            algtype = form_dict["type"]
            jobname = form_dict['name']
            maxflops = int(form_dict['modelsize'])
            datasetid = form_dict['dataSelection']
            if form_dict['dataSelection'] != None:
                datasetname = models.Dataset.objects.filter(id = int(datasetid))[0]
                # print(datasetname.name)
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
                #back_untils.alg_cp(r'./../../algorithm/classification/pytorch_automodel/image_classification',"")

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
                jobid = API_tools.get_keyword(str(info["payload"]["jobId"]))
                name = API_tools.get_keyword(str(jobname))
                username = API_tools.get_keyword(str(user.username))
                user_id = str(user.id)
                state = "WAITTING"
                createdTime = API_tools.get_keyword(str(otherStyleTime))
                completedTime = str(0)
                _path = API_tools.get_keyword(str(outputdir))
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
    # 路径选择器对接的后端
    # 使用 os 包
    # 需要注意用户权限的问题
    home="/home/pcl/wyh_project/PCL_AutoML_System/zdebug"
    select_dir=True
    
    def get(self,request):
        # limit user-visible directory
        # root="/home/pcl/wyh_project/PCL_AutoML_System/debug"
        params=request.query_params.dict()
        # print("Params is:",params)
        raw=params['0']
        if raw.startswith("~"):
            pass
        now,prefix=os.path.split(raw)
        if raw.endswith("..") or prefix=="..":
            now,prefix=os.path.split(now)
        # print("Path is: ",os.path.join(self.home,now))
        try:
            file_list=os.listdir(os.path.join(self.home,now))
            file_list=[os.path.join(now,v) for v in file_list if v.startswith(prefix)]
            for i,item in enumerate(file_list):
                if os.path.isdir(os.path.join(self.home,item)) and item[-1]!="/":
                    file_list[i]+="/"
        except FileNotFoundError:
            file_list=[
                "路径不存在，请返回上级路径或返回到home路径：",
                "..",
                "~"
            ]
            file_list=Parser(file_list)
            return Response(data=file_list)
        # if file_list
        
        res=[os.path.join(now,"..")]+file_list
        # print("Res is: ",res)
        res=Parser(res)
        return Response(data=res)

class RefreshAlgo(APIView):
    def get(self,request):
        user=auth.get_user(request)
        # print(request.data)
        params=request.query_params.dict()
        if not params.__contains__('algo_id'):
            return Response(data=[])
        print("ALGO ID: ", params['algo_id'])
        try:
            algo=models.customize_algo.objects.get(id=params['algo_id'])
        except:
            return Response(data=[])
        reps=[]
        if params.__contains__('hyper'):
            hypers=algo.algo_hpyer_set.all()
            for hyper in hypers:
                # print("HYPER is: ",hyper.__dict__)
                reps.append({
                    "id":hyper.id,
                    "name":hyper.name,
                    "dataType":hyper.data_type,
                    "default":hyper.initial_value,
                    "necessray":hyper.is_necessary,
                    # "predefined":True
                })
        elif params.__contains__('ioput'):
            # print("GET IO infos")
            ios=algo.algo_io_set.all()
            for io in ios:
                reps.append({
                    "id":io.id,
                    "label":io.fname,
                    "name":io.name,
                    # "predefined":True
                })
        response=Parser(reps)
        return Response(data=response)
    
class RefreshResource(APIView):
    def get(self,request):
        user=auth.get_user(request)
        # print(request.data)
        params=request.query_params.dict()
        # print("PARAMS: ",params)
        reps=[]
        # 得到云脑平台的资源类型，返回给前端
        for i,x in enumerate(RES_TYPE):
            if not i : continue
            tag=["GPU: ","CPU:","Memory:","Shared Memory:"]
            # num=[j if j <1024]
            num=x
            label=", ".join([ l+str(n) for l,n in zip(tag,num)])
            reps.append({
                "label": label,"value": i,
            })
        # response["total"]=len(reps)
       
        return Response(data=reps)

class RefreshMethod(APIView):
    def get(self,request):
        user=auth.get_user(request)
        # print(request.data)
        params=request.query_params.dict()
        # print("PARAMS: ",params)
        reps=[]
        for n in METHODS:
            reps.append({'label':n,'value':n})
        return Response(data=reps)
    
def DictCheck(src:dict, keys:list):
    ''' 判断src是否符合标准，即字典中必须存在keys里的键，且值对应的长度不为0，
    '''
    result=True
    for k in keys:
        if not src.__contains__(k) or not len(src[k]):
            result=False
            break
    return result

class AlgoManage(APIView):
    def get(self, request):
        user=auth.get_user(request)
        query=request.data
        print(query)
        # # 
        algo_sets=models.customize_algo.objects.filter(uid=user)
        # print(type(algo_sets[0]))
        algo_list=[]
        for rec in algo_sets:
            algo_list.append({
                "id": rec.id,
                "name": rec.name,
                "version": rec.version,
                "description": rec.description,
                "created_at": rec.created_at,
            })
        # # 
        result=algo_list # 注意！ 返回值必须是数组形式的 否则前端会报错： RawData.some is not function
        response=Parser(result)
        return Response(data=response)

    def post(self,request):
        user = auth.get_user(request)
        form_dict=request.data
        print("Get algo create: ",form_dict)
        name=form_dict['name']
        version=form_dict['version']
        aiEngine= "-".join(form_dict['AIEngine'])
        codePath=form_dict['CodePath']
        startPath=form_dict['StartFile']
        hyperList=form_dict['hyperParams']
        ioList=form_dict['inputParams']
        algo_list=models.customize_algo.objects.filter(name=name)
        if len(algo_list):
            for algo in algo_list:
                unique="-".join([algo.name,algo.version])
                if unique == "-".join([name.strip(),version.strip()]):
                    res=errParser(errmessage="\"算法名称-版本\"已存在，请修改名称或版本")
                    return Response(data=res)                    
        newAlgo=models.customize_algo.objects.create(
            name=name,
            version=version,
            ai_engine=aiEngine,
            project_path=codePath,
            start_path= startPath,
            uid=user,
        )
        for item in hyperList:
            newHyper=models.algo_hpyer.objects.create(
                name=item['name'],
                data_type=item['dataType'],
                initial_value=item['default'] if item.__contains__('default') else '',
                is_necessary= True if item.__contains__('necessray') and item['necessray'] else False,
                belong_algo=newAlgo,
            )
        for item in ioList:
            print(type(item))
            newIO=models.algo_io.objects.create(
                fname=item['label'],
                name=item['name'],
                # version=item['version'], 
                default_path=item['default'] if item.__contains__('default') else '',
                description=item['description'] if item.__contains__('description') else '',
                belong_algo=newAlgo,
            )
        res=[]
        res=Parser(res)
        return Response(data=res)    
    def delete(self, request):
        user = auth.get_user(request)
        print(user)
        form_dict=request.data
        print("DELETE is: ",form_dict)
        try:
            algo=models.customize_algo.objects.get(id=form_dict['id'])
            # algo=models.customize_algo.objects.get(id=10001)
        except BaseException as e:
            res=errParser(errmessage=repr(e))
        else:
            if all([
                algo.name == form_dict['name'],
                # algo.created_at == form_dict['created_at'],
                True,
            ]):
                print("DELETE SELETED ALGO")
                algo.delete()
            res=[]
            res=Parser(res)
        return Response(data=res)    

def parse_param(form_dict):
    res=None
    param={}
    if form_dict.__contains__("hyperDict"):
        for item in form_dict["hyperDict"]:
            n=item['name']
            v=item['default']
            if param.__contains__(n):
                res=errParser(errmessage="有重名的参数:{}".format(item['name']))
            # 之后的类型检查
            if   item['dataType'] == 'int':
                pass
            elif item['dataType'] == 'float':
                pass
            elif item['dataType'] == 'string':
                pass
            elif item['dataType'] == 'bool':
                pass
            param[n]=v
    if form_dict.__contains__("ioDict"):
        for item in form_dict["ioDict"]:
            n=item['name']
            v=item['path']
            if param.__contains__(n):
                res=errParser(errmessage="有重名的参数:{}".format(item['name']))
            param[n]=v       
    return param, res
class TrainJobManage(APIView):

    def get(self, request):
        print("GET Train Job Manage")
        user = auth.get_user(request)
        back_untils.refresh_train_job(user)
        # back_untils.update_train_job(user.tocken,user.username,user.first_name)
        job_set=models.customize_job.objects.filter(uid=user)
        job_list=[]
        for rec in job_set:
            algo=rec.algo_id
            algo_name= " : ".join([algo.name,algo.version]) if algo else ""
            # print("ALGO is: ", rec.algo_id)
            job_list.append({
                "id": rec.id,
                "name":rec.name,
                "status":rec.state.lower(),
                "created_at":rec.created_at,
                "completed_at":rec.completed_at,
                "algo":algo_name,
            })
        result=job_list
        response=Parser(result)
        return Response(data=response)  
    
    def delete(self, request):
        user = auth.get_user(request)
        # print(user)
        form_dict=request.data
        print(form_dict)
        try:
            job=models.customize_job.objects.get(id=form_dict['id'])
            rep=API_tools.delete_job(job.job_id,user.tocken,user.username,user.first_name)
            if rep['code']!="S000":
                # raise Exception(rep['msg'])
                raise Exception("只能让任务停止，无法删除任务")
            print("DELETE Result: ",rep)
            res=Parser([])
        except BaseException as e:
            res=errParser(errmessage=repr(e))
        finally:
            return Response(data=res)   
     
    def post(self,request):
        # 创建任务
        # 后送到云脑
        # 成功后再录入数据库
        user = auth.get_user(request)
        form_dict=request.data
        print("MISSION DICT: ",form_dict)
        name=form_dict["name"]
        try:
            algo=models.customize_algo.objects.get(id=form_dict["algoID"])
        except BaseException as e:
            print("DATABASE ERROR:",repr(e))
            res=errParser()
            return Response(data=res)
        project_path=algo.project_path
        main_file=algo.start_path         
        param,res=parse_param(form_dict)
        if res:
            return Response(data=res)    
        index=form_dict['resource']
        resource={ k:v for k,v in zip(RES_TYPE[0],RES_TYPE[index])}
    
        info=API_tools.mission_submit(
            job_name=name.lower(),
            project_dir=project_path,
            main_file=main_file,
            param=param,
            resource=resource,
            username=user.username, 
            password=user.first_name,
        ) 
        print("TYPE is: ", type(info))
        print("RETURN INFO IS: ", info)
        '''RETURN INFO IS: {
            'code': 'S000', 
            'msg': 'update job kktestnet2 successfully', 
            'payload': {
                'jobId': 'fbb98fc00e9d0011eb0891304939b5259323'}}'''
        if type(info) != dict or info.__contains__("code") and info["code"]!="S000":
            res=errParser(errmessage="")
        else: 
            job=info['payload']
            # print("JOB INFO: ",job)
            res=back_untils.insert_train_job(user,job["jobId"],algo)
            res=errParser(errmessage=res[0]) if len(res) else Parser(res)
        return Response(data=res)    
def format_range(type,ranger):
    res=ranger
    return res

# def search_mission(method:str,hyper:dict,package:dict,api_config:dict):
#     print("========MISSION REPORT========")
#     print("METHOD is: ",method)
#     print("-"*24)
#     print("Hypers: ")
#     a=[print(k,v) for k,v in hyper.items()]
#     print("-"*24)
#     print("Job config is: ")
#     a=[print(k,v) for k,v in package.items()]
#     print("-"*24)
#     print("BBO config is: ")
#     a=[print(k,v) for k,v in api_config.items()]
#     print("="*24)
#     return False

class AutoJobManage(APIView):
    def get(self, request):
        user = auth.get_user(request)
        job_list=[]
        try:
            job_set=models.customize_auto_search.objects.filter(uid=user)
        except BaseException as e:
            print("Auto Search Dataset Exception: ",repr(e))
            response=errParser(errmessage=repr(e))
        else:
            for rec in job_set:
                algo=rec.algo_id
                algo_name= " : ".join([algo.name,algo.version]) if algo else ""                
                job_list.append({
                    "id": rec.id,
                    "name":rec.name,
                    "status":rec.state.lower(),
                    "created_at":rec.created_at,
                    "completed_at":rec.completed_at,
                    "algo":algo_name,
                })
            result=job_list
            response=Parser(result)
        return Response(data=response)
    def post(self,request):
        '''
            type : {'real', 'int', 'cat', 'bool'}
            space : {'linear', 'log', 'logit', 'bilog'}
            range : (lower, upper) 
            values : []
            
            # either range or values 
            # real/int: range-space / values
            # cat: must be values
            # bool: does not take anything extra ( space , range , or values )
        '''
        '''
        form_dict={
            'name':, # normal
            'method':, # BBO method used for search           
            'suggest':, # hyper: number of suggestion
            'epoch':, # hyper: search epoch
            'result':, # Search result: result.txt path
            'algo':{
                'id':,
                'hyperDict':[], # same as TrainJobManage
                'ioDict':[], # same as TrainJobManage
                },
            'search_para':[
                {   
                    'id':,
                    'name':, 
                    'dataType':, 
                    'space':, 
                    'searchType':'values'|'range', 
                    'content':'x x x x x',
                },
                ...
            ],
            'resource':, # same as TrainJobManage
        }
        '''
        user = auth.get_user(request)
        form_dict=request.data
        print("DICT is: ",form_dict)
        # return Response(data=Parser([]))

        pid=0
        start=False
        hyper={}
        hyper['suggest']=form_dict['suggest']
        hyper['epoch']  =form_dict['epoch']
        hyper['result'] =form_dict['result']
        # Parse the parameters of create a mission
        algoDict=form_dict['algo']
        algo=models.customize_algo.objects.get(id=algoDict['id'])
        name=form_dict['name']
        index=form_dict['resource']
        resource={ k:v for k,v in zip(RES_TYPE[0],RES_TYPE[index])}
        param,res=parse_param(algoDict)
        if res: return Response(data=res)
        package={
            'job_name':name, # 搜索算法系列任务的 prefix 名
            'project_dir':algo.project_path,
            'main_file':algo.start_path,
            'param':param, # 未被作为搜索对象的参数
            'resource':resource,
            'username':user.username,
            'password':user.first_name,
            } 
        # Set the API_config of search 指定要搜索的参数及其范围
        search_config={} # Follow the structure of "API of BBO"
        # for item in form_dict['search_para']:
            # d={'type':item['dataType']}
            # t=copy.deepcopy(item)
            # del t['id'], t['default'], t['name'], t['dataType'], t['necessary']
            # t['range']=format_range(d['type'],t['range'])
            # search_config[item['name']]={**d,**t} # 合并展开成为搜索用的字典
            # print("SEARCH Config: ",item['name'],
            #       search_config[item['name']],d)
        def num(inp:str,typer):
            # 1. 整形数 123 -10
            # 2. 浮点数 1.23 -2.21
            # 3. 科学计数 1e-4 1e20
            return inp
        def parse_values(content,typer):
            res=content.split(' ')
            return [num(x,typer) for x in res ]

        for item in form_dict['search_para']:
            search_config[item['name']]={
                'type': 'real'if item['dataType'] == 'float' else item['dataType'],
            }
            content=parse_values(item['content'],item['dataType'])
            if item['searchType']=='values':
                search_config[item['name']]['values']=content
                pass # 所有的数作为选择范围
            elif item['searchType']=='range':
                search_config[item['name']]['range']=content[:2]
                search_config[item['name']]['space']=item["space"]
                pass # 前两个数作为范围
            # if item.__contains__('space'):
            #     search_config[item['name']]['space']=item["space"]
            # if item.__contains__('range'):
            #     search_config[item['name']]['range']=item["range"]
            # if item.__contains__('space'):
            #     search_config[item['name']]['space']=item["space"]
                
                
        # Start Search
        # # Start a process
        start=back_untils.search_mission(PLIST,form_dict['method'],hyper,package,search_config)
        start=False
        # os.fork
        # If Success
        # Append to database
        # # ["waiting","running","succeeded","failed","stopped"]
        if start:
            models.customize_auto_search.objects.create(
                name=form_dict['name'],
                state="running",
                algo_id=algo,
                uid=user,
                suggest=form_dict['suggest'],
                epoch=form_dict['epoch'],
                pid=pid,
            )
            res=Parser([])
        else:
            res=errParser(errmessage="Failed to start")
        return Response(data=res)
        pass 
    
    
# class AIMarket(APIView):
#     def get(self, request):
#         """
#         login get
#         """
#         #公开算法数据库内容[{}{}{}]
        
#         params=request.query_params.dict()
#         print(params)
        
#         rec = []
#         queryset = models.Algorithm.objects.all()
        
#         # if(not len(queryset)):# 返回伪造数据
#         if(True):# 返回伪造数据
#             result=mock.genAlgoList()
#             # result=mock.ALGORITHM_LIST
#         else:
#         # Algo={
#             #     'id' ,
#             #     'name' ,
#             #     'task' ,
#             #     'path',
#             #     'created_at',
#             #     'uid',}
#             ret = AlgorithmSerializers(queryset, many=True) # 
#             print("%ret%", "%ret%", type(ret.data), type(ret.data[0]))
#             for onejob in ret.data:

#                 rec.append(
#                     {
#                         'id':onejob["id"],
#                         'name':onejob["name"],
#                         'task':onejob["task"],
#                         "path":onejob["_path"],
#                     }
#                 )
#             result = rec
        
#         # 对get回传的筛选/搜索参数进行处理
        
#         # 开始搜索
        
#         # 开始筛选
#         for item in result:
#             ids=item['uid']
#             del item['uid']
#             # 这里应该从数据库里query 创建者的名字
#             item['createUser']=mock.USER_LIST[ids]
#         # result=result
#         result=Parser(result)
#         return Response(data=result)

#     def post(self,request):
#         form_dict=request.data
#         print(form_dict)
#         # 回传的筛选条件 - 字典形式
#         # name type dataRange createUser
        
#         result=mock.genAlgoList()
#         # result=mock.ALGORITHM_LIST

#         if(not len(form_dict)): # 此时说明重置，返回所有已查询
#             pass
#         else: # 进行条件过滤
#             pass
#         for item in result:
#             ids=item['uid']
#             del item['uid']
#             # 这里应该从数据库里query 创建者的名字
#             item['createUser']=mock.USER_LIST[ids]        
#         result=Parser(result)
#         return Response(data=result)
 
# class UserAlgorithm(APIView):
#     def get(self, request):
#         """
#         login get
#         """
#         #公开算法数据库内容[{}{}{}]
#         rec = []
#         queryset = models.User_algorithm.objects.all()
#         ret = UAlgorithmSerializers(queryset, many=True)
#         print("%ret%", "%ret%", type(ret.data), type(ret.data[0]))
#         for onejob in ret.data:

#             rec.append(
#                 {
#                     'id':onejob["id"],
#                     'name':onejob["name"],
#                     'task':onejob["task"],
#                     "_path":onejob["_path"],
#                 }
#             )
#         result = rec
#         pass
#     def post(self,request):
#         pass

# class PubDataset(APIView):
#     def get(self, request):
#         """
#         login get
#         """
#         #公开算法数据库内容[{}{}{}]
#         rec = []
#         queryset = models.Dataset.objects.all()
#         ret = DatasetSerializers(queryset, many=True)
#         print("%ret%", "%ret%", type(ret.data), type(ret.data[0]))
#         for onejob in ret.data:

#             rec.append(
#                 {
#                     'id':onejob["id"],
#                     'name':onejob["name"],
#                     'task':onejob["task"],
#                     "_path":onejob["_path"],
#                 }
#             )
#         result = rec
#         pass
#     def post(self,request):
#         pass
    
# class DataManage(APIView):
#     def get(self, request):
#         """
#         login get
#         """
#         pass
#     def post(self,request):
#         pass 
    
# class DevEnv(APIView):
#     def get(self, request):
#         """
#         login get
#         """
#         pass
#     def post(self,request):
#         pass 
    
# class ModelManage(APIView):
#     def get(self, request):
#         """
#         login get
#         """
#         pass
#     def post(self,request):
#         pass 
