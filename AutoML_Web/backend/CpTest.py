# coding=utf-8

import os,sys,stat
import shutil
import time
'''
if os.path.exists('~/wdc_mnt/jobspace') !=True:
    os.makedirs('~/wdc_mnt/jobspace')
if os.path.exists('~/wdc_mnt/jobspace/algorithm') !=True:
    os.makedirs('~/wdc_mnt/jobspace/algorithm')
if os.path.exists('~/wdc_mnt/jobspace/classification') !=True:
    os.makedirs('~/wdc_mnt/jobspace/classification')

old_path = r'~/wdc_mnt/PCL_AutoML/PCL_AutoML_System/algorithm/classification/pytorch_image_classification'
new_path = r'~/wdc_mnt/jobspace/algorithm'
'''

def alg_cp(source,target):
    #jobspace / algorithm /classification/pytorch_automodel/
    if os.path.exists(r'~/wdc_mnt/jobspace') != True:
        os.makedirs(r'~/wdc_mnt/jobspace')
    if os.path.exists(r'~/wdc_mnt/jobspace/algorithm') != True:
        os.makedirs(r'~/wdc_mnt/jobspace/algorithm')
    if os.path.exists(r'~/wdc_mnt/jobspace/algorithm/classification') != True:
        os.makedirs(r'~/wdc_mnt/jobspace/algorithm/classification')
    if os.path.exists(r'~/wdc_mnt/jobspace/algorithm/classification/pytorch_automodel') != True:
        os.makedirs(r'~/wdc_mnt/jobspace/algorithm/classification/pytorch_automodel')

    #print(os.system("mkdir stest"))

    os.chmod(r'~/wdc_mnt/jobspace/algorithm/classification/pytorch_automodel',
             stat.S_IRWXO + stat.S_IRWXG + stat.S_IRWXU)
    os.chmod(r'~/wdc_mnt/PCL_AutoML/PCL_AutoML_System/algorithm/classification/pytorch_automodel/image_classification',
             stat.S_IRWXO + stat.S_IRWXG + stat.S_IRWXU)

    source_path = os.path.abspath(r'~/wdc_mnt/PCL_AutoML/PCL_AutoML_System/algorithm/classification/pytorch_automodel/image_classification')
    target_path = os.path.abspath(r'~/wdc_mnt/jobspace/algorithm/classification/pytorch_automodel')

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
alg_cp("","")