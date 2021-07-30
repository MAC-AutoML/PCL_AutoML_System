# coding=utf-8

import os,sys,stat
from multiprocessing import Process,pool
import shutil
import time
import datetime
from django.db import models as dmodel
from _app import models

from tools import API_tools
from  tools.API_tools import get_keyword

def AutoSearch(method:str,hyper:dict,package:dict,api_config:dict):
    print("子进程（%s） 开始执行，父进程为（%s）" % (os.getpid(), os.getppid()))
    time.sleep(20)
    print("========MISSION REPORT========")
    print("pid: %s METHOD is: "%(os.getpid()),method)
    time.sleep(20)
    print("-"*24)
    time.sleep(20)
    print("pid: %s Hypers: "%(os.getpid()))
    a=[print(k,v) for k,v in enumerate(hyper.items())]
    print("-"*24)
    time.sleep(20)
    print("pid: %s Job config is: "%(os.getpid()))
    a=[print(k,v) for k,v in package.items()]
    print("-"*24)
    time.sleep(20)
    print("pid: %s BBO config is: "%(os.getpid()))
    a=[print(k,v) for k,v in api_config.items()]
    print("="*24)
    
class SearchPool(pool.Pool):
    def __init__(self, processes:int, method:str,hyper:dict,package:dict,api_config:dict) -> None:
        super().__init__(processes=processes)
        self.method=method
        self.hyper=hyper
        self.package=package
        self.api_config=api_config
        self.result=[]
    def __del__(self):
        print("EXIT POOLS")
        self.close()
        self.terminate()
        super().__del__()
    def add_mission(self):
        res=self.apply_async(AutoSearch,args=(self.method,self.hyper,self.package,self.api_config))
        self.result.append(res)
    def show_result(self):
        a=[print(x) for x in self.result]
class SearchProcess(Process):
    def __init__(self,method:str,hyper:dict,package:dict,api_config:dict ) -> None:
        super().__init__()
        self.method=method
        self.hyper=hyper
        self.package=package
        self.api_config=api_config
        self.state=True
    def run(self):
        AutoSearch(self.method,self.hyper,self.package,self.api_config)
              
def updata_user_algorithm(user,id):
    u_alg = models.User_algorithm.objects.exclude(algorithm_id=None).filter(user_id=id)
    p_alg = models.Algorithm.objects.all()
    uid = id
    fk = []
    pk = []
    for it in u_alg:
        fk.append(it.algorithm_id)
    for it in p_alg:
        pk.append(it.id)
    print("fk and pk:",fk,pk)
    for it in pk:
        print("it",it)
        if it not in fk:
            palobj = models.Algorithm.objects.filter(id=it)[0]
            ujb = models.User_algorithm.objects.create(algorithm_id = it,user_id=uid,name=palobj.name,task=palobj.task,_path=palobj._path)
            ujb.save()

def updata_jobtable(tocken,un,pa,typer="automl"):
    # 对于正在运行中的任务，更新他们的状态
    #同步云脑数据库job信息
    if typer == "automl":
        job = models.User_Job.objects.all().order_by("id")
    else:
        job = models.customize_job.objects.all().order_by("id")
    job = job.exclude(state="STOPPED").exclude(state="FAIL").exclude(state="SUCCEEDED")
    for jd in job:
        print(jd)
        jobid=jd.jobid if typer=="automl" else jd.job_id
        jd_detail = API_tools.get_jobinfo(jobid,tocken,un,pa)
        if jd_detail["code"] == "S000":
            jd.state = jd_detail["payload"]["jobStatus"]["state"]
            timeStamp2 = int(jd_detail['payload']['jobStatus']["completedTime"])
            if timeStamp2 != 0:
                timeArray2 = time.localtime(timeStamp2 / 1000)
                otherStyleTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray2)
                jd.completedTime = otherStyleTime2
            jd.save()
            print("$$$$$$$$ Update Dataset Success")

def refresh_train_job(user):
    '''
    Args:
        user: 用户实例
    '''
    # 以本地数据库的信息为主
    un=user.username
    pa=user.first_name
    token=API_tools.get_tocken(un,pa)
    job_list=models.customize_job.objects.all()
    for rec in job_list:
        # print("JOB: ", rec.jobid)
        info=API_tools.get_jobinfo(rec.job_id,token,un,pa)
        if info['code'] == 'S000': # 存在该任务
            job=info['payload']
            rec.state = job["jobStatus"]["state"]
            timeStamp2 = int(job['jobStatus']["completedTime"])
            if timeStamp2 == 0: continue
            rec.completed_at = datetime.datetime.fromtimestamp(
                timeStamp2/1000 )
            rec.save()            
        else:
            rec=models.customize_job.objects.get(id=rec.id)
            rec.delete()
            
def insert_train_job(user,job_id,algo=None):
    res_info=API_tools.get_jobinfo(job_id,"",user.username,user.first_name)
    job=res_info["payload"]
    print("RESPONSE JOB INFO: ",res_info)
    jid=job['id']
    if jid != job_id:
        return ["Job id Error"]
    createdTime = datetime.datetime.fromtimestamp(job['jobStatus']["completedTime"]/1000) 
    # compeletedTime = createdTime
    
    models.customize_job.objects.create(
        job_id=jid,
        name=job['name'],
        state=job['jobStatus']['state'],
        created_at=createdTime,
        # completed_at=compeletedTime,
        uid=user,
        algo_id=algo,
    )    
    return []    

def info_decoder(job_info):
    pass
def alg_cp(source,target):
    #jobspace / algorithm /classification/pytorch_automodel/
    if os.path.exists(r'/home/pcl/wdc_mnt/jobspace') != True:
        os.makedirs(r'/home/pcl/wdc_mnt/jobspace')
    if os.path.exists(r'/home/pcl/wdc_mnt/jobspace/algorithm') != True:
        os.makedirs(r'/home/pcl/wdc_mnt/jobspace/algorithm')
    if os.path.exists(r'/home/pcl/wdc_mnt/jobspace/algorithm/classification') != True:
        os.makedirs(r'/home/pcl/wdc_mnt/jobspace/algorithm/classification')
    if os.path.exists(r'/home/pcl/wdc_mnt/jobspace/algorithm/classification/pytorch_automodel') != True:
        os.makedirs(r'jobspace/algorithm/classification/pytorch_automodel')
    if os.path.exists(r'/home/pcl/wdc_mnt/jobspace/algorithm/classification/pytorch_automodel/image_classification') != True:
        os.makedirs(r'jobspace/algorithm/classification/pytorch_automodel/image_classification')
    print("###", os.path.exists(r'/home/pcl/wdc_mnt/jobspace/algorithm/classification/pytorch_automodel/image_classification'))

    #print(os.system("mkdir stest"))

    os.chmod(r'/home/pcl/wdc_mnt/jobspace/algorithm/classification/pytorch_automodel',
             stat.S_IRWXO + stat.S_IRWXG + stat.S_IRWXU)
    os.chmod(r'/home/pcl/wdc_mnt/PCL_AutoML/PCL_AutoML_System/algorithm/classification/pytorch_automodel/image_classification',
             stat.S_IRWXO + stat.S_IRWXG + stat.S_IRWXU)

    source_path = os.path.abspath(r'/home/pcl/wdc_mnt/PCL_AutoML/PCL_AutoML_System/algorithm/classification/pytorch_automodel/image_classification')
    target_path = os.path.abspath(r'/home/pcl/wdc_mnt/jobspace/algorithm/classification/pytorch_automodel')

    def del_file(filepath):
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    del_file(target_path)
    os.rmdir(target_path)

    shutil.copytree(source_path, target_path)

    print('$$$$$$$$$$$$$$$$$Copy files finished!')

def search_mission(plist:list,method:str,hyper:dict,package:dict,api_config:dict):
    p=SearchProcess(method,hyper,package,api_config)
    p.start()
    if p.is_alive():
        print("SubProcess Success")
        plist.append(p)
        return True
    else:
        print("SubProcess Failed")
        return False
def search_mission_pool(method:str,hyper:dict,package:dict,api_config:dict):
    pass    