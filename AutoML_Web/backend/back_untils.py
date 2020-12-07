# coding=utf-8

import os,sys,stat
import shutil
import time
from _app import models
import time
from tools import API_tools
from  tools.API_tools import get_keyword


def updata_jobtable(tocken,un,pa):
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