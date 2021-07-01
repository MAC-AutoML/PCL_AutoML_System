import requests
import json
import re

def bytes2dict(response):
    info = json.loads(response.content)
    print("INFO:",info)
    return info

def get_keyword(s):
    if "'" in s:
        result = re.findall(".*'(.*)'.*", s)
        return result[0]
    else:
        return s

def get_tocken(uname,password):
    url = 'http://192.168.204.24/rest-server/api/v1/token'

    data = {
      "username": str(uname),
      "password": str(password),
    }
    data = str(data).replace('\'','"')
    print(type(data),data)
    response = requests.post(url=url, json=json.loads(data))

    info = bytes2dict(response)
    if info["code"] != 'S000':
        return "用户名或密码错误"
    return "Bearer "+info["payload"]["token"]

def check_user(username,password):
    tocken = get_tocken(username,password)
    if "错误" in tocken:
        return tocken
    headers = {
        "Content-Type": 'application/json',
        "Authorization": tocken
    }

    url = "http://192.168.204.24/rest-server/api/v1/user/" + username
    response = requests.get(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    return info

def get_userinfo(username,tocken,password):
    tocken = get_tocken(username,password)
    if "错误" in tocken:
        return tocken
    headers = {
        "Content-Type": 'application/json',
        "Authorization": tocken
    }

    url = "http://192.168.204.24/rest-server/api/v1/user/" + username
    response = requests.get(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    return info

def get_joblist(tocken,username,password,size=20,offset=0):
    tocken = get_tocken(username,password)
    headers = {
        "Content-Type": 'application/json',
        "Authorization": tocken
    }
    url = "http://192.168.204.24/rest-server/api/v1/jobs?size="+str(size)+"&offset="+str(offset)
    response = requests.get(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    return info["payload"]

def get_jobinfo(jobid,tocken,username,password):
    headers = {
        "Content-Type": 'application/json',
        "Authorization": get_tocken(username,password)
    }
    url = "http://192.168.204.24/rest-server/api/v1/jobs/" + str(jobid)
    response = requests.get(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    return info
def mission_submit(job_name, project_dir, param, resource, username, password):

    url = f'http://192.168.204.24/rest-server/api/v1/jobs'

    tocken = get_tocken(username, password)
    command = f"cd {project_dir} && python {param['main_file']}"
    for k, v in param.items():
        if k != 'main_file' and k != 'image':
            command += f' --{k} {v}'

    data = \
        f"""
    {{
    "jobName": "{job_name}",
    "retryCount": 0,
    "gpuType": "dgx",
    "image": "{param['image'] if "image" in param.keys() else "dockerhub.pcl.ac.cn:5000/user-images/wudch:1.2"}",
    "taskRoles": [
        {{
        "taskNumber": 1,
        "minSucceededTaskCount": 1,
        "minFailedTaskCount": 1,
        "cpuNumber": {resource["cpuNumber"] if "cpuNumber" in resource.keys() else 2},
        "gpuNumber": {resource["gpuNumber"] if "gpuNumber" in resource.keys() else 1},
        "memoryMB": {resource["memoryMB"] if "memoryMB" in resource.keys() else 4096},
        "shmMB": {resource["shmMB"] if "shmMB" in resource.keys() else 4096},
        "command": "{command}",
        "name": "main",
        "needIBDevice": false,
        "isMainRole": false
        }}
    ]
    }}
    """
    headers = {
        "Content-Type": 'application/json',
        "Authorization": tocken
    }
    response = requests.post(url=url, json=json.loads(data), headers=headers)
    info = bytes2dict(response)
    if info["code"] != 'S000':
        return "Unexpected error"
    else:
        jobId = info['payload']['jobId']
        urljob = f'http://192.168.204.24/rest-server/api/v1/jobs/{jobId}'
        jobResponse = requests.get(url=urljob, json={}, headers=headers)
        jobInfo = bytes2dict(jobResponse)
        if jobInfo["code"] != "S000":
            return "Unexpected error"
        else:
            return jobInfo


def creat_mission(job_name, command,tocken,username,password):
    url = f'http://192.168.204.24/rest-server/api/v1/jobs/{job_name}'

    print(url)
    data = \
        f"""
    {{
    "jobName": "{job_name}",
    "retryCount": 0,
    "gpuType": "dgx",
    "image": "dockerhub.pcl.ac.cn:5000/user-images/wudch:1.2",
    "taskRoles": [
        {{
        "taskNumber": 1,
        "minSucceededTaskCount": 1,
        "minFailedTaskCount": 1,
        "cpuNumber": 2,
        "gpuNumber": 1,
        "memoryMB": 4096,
        "shmMB": 4096,
        "command": "{command}",
        "name": "random",
        "needIBDevice": false,
        "isMainRole": false
        }}
    ]
    }}
    """
    headers = {
        "Content-Type": 'application/json',
        "Authorization": get_tocken(username,password)
    }
    response = requests.put(url=url, json=json.loads(data), headers=headers)
    info = bytes2dict(response)
    return info

def delete_job(jobid,tocken,username,password):
    headers = {
        "Content-Type": 'application/json',
        "Authorization": get_tocken(username,password)
    }
    url = "http://192.168.204.24/rest-server/api/v1/jobs/" + str(jobid)
    response = requests.delete(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    return info

if __name__ == "__main__":
    command = "cd ../userhome/network-pruning-rfm-master/cifar/l1-norm-pruning/&&PYTHONPATH=./ python main.py --dataset cifar10 --arch vgg --depth 16 --save './log/ori_vgg16'"
    #creat_mission("rua",command)
    #a = get_joblist("wudch")
    #print("a",a["jobs"][0])
    #import time
    '''
    otherStyleTime = 0
    item = a["jobs"][0]
    timeStamp = time.time()
    print(timeStamp/1000)
    timeArray = time.localtime()
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    item["createdTime"] = otherStyleTime
    print(item["createdTime"])
    print(a["jobs"][0])
    print("######",otherStyleTime)
    newjobinfo = get_jobinfo(a["jobs"][0]["id"])
    print(newjobinfo)
    import re
    str = "qweq('deafeaf'),eqwe"
    result = re.findall(".*'(.*)'.*", str)
    print(result[0])'''
    #UID = 1
    #print(check_user("wudch", "woodchen"))
    jbl = get_joblist("","wudch", "woodchen",size=10,offset=0)
    print("#######")
    print(jbl)
    jbd = get_jobinfo("19760a900392d011eb0b03c0e1c553706053","","wudch", "woodchen")
    print("##########")
    print(jbd)

    headers = {
        "Content-Type": 'application/json',
        "Authorization": get_tocken("wudch", "woodchen")
    }
    url = "http://192.168.204.24/rest-server/api/single/log?job=flops9000test&taskName=random&taskPod=19760a900392d011eb0b03c0e1c553706053-random-0-0-0"
    response = requests.get(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    print("#####!!")
    print(info)