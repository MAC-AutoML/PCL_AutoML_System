# coding=utf-8

import os,sys,stat
import shutil
import time
import datetime
from _app import models
from tools import API_tools
from  tools.API_tools import get_keyword

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


def updata_jobtable(tocken,un,pa):
    # 对于正在运行中的任务，更新他们的状态
    #同步云脑数据库job信息
    job = models.User_Job.objects.all().order_by("id")
    job = job.exclude(state="STOPPED").exclude(state="FAIL").exclude(state="SUCCEEDED")
    for jd in job:
        print(jd)
        jd_detail = API_tools.get_jobinfo(jd.jobid,tocken,un,pa)
        if jd_detail["code"] == "S000":
            jd.state = jd_detail["payload"]["jobStatus"]["state"]
            timeStamp2 = int(jd_detail['payload']['jobStatus']["completedTime"])
            if timeStamp2 != 0:
                timeArray2 = time.localtime(timeStamp2 / 1000)
                otherStyleTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray2)
                jd.completedTime = otherStyleTime2
            jd.save()
            print("$$$$$$$$ Update Dataset Success")
def refresh_jobtable(tocken,un,pa,user):
    # user 是 auth.user 对象
    # 从云脑API处获取所有的任务，
    job_list=API_tools.get_joblist(tocken,un,pa,size=20,offset=0)

    totalSize=job_list["totalSize"]
    job_list=job_list["jobs"]
    
    now_jobs=models.customize_job.objects.all()
    ids=[j.job_id for j in now_jobs]
    ids=set(ids)
    for job in job_list:
        if job['id'] in ids:
            continue
        # ! 这里没有指定时区，默认是使用当地时区，也就是北京时间
        createdTime= datetime.datetime.fromtimestamp(job["createdTime"]/1000) 
        compeletedTime=datetime.datetime.fromtimestamp(job["completedTime"]/1000)
        
        models.customize_job.objects.create(
            job_id=job["id"],
            name=job["name"],
            state=job["state"],
            created_at=createdTime,
            completed_at=compeletedTime,
            uid=user,
        )
    pass
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