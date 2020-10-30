import requests
import json

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

def get_tocken():
    url = 'http://192.168.204.24/rest-server/api/v1/token'

    data = """{
      "username": "wudch",
      "password": "woodchen"
    }"""
    response = requests.post(url=url, json=json.loads(data))
    info = bytes2dict(response)
    return "Bearer "+info["payload"]["token"]

def get_userinfo(uname):
    tocken = get_tocken()
    headers = {
        "Content-Type": 'application/json',
        "Authorization": tocken
    }

    url = "http://192.168.204.24/rest-server/api/v1/user/" + uname
    response = requests.get(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    return info

def get_joblist(username,size=20,offset=0):
    tocken = get_tocken()
    headers = {
        "Content-Type": 'application/json',
        "Authorization": tocken
    }
    url = "http://192.168.204.24/rest-server/api/v1/jobs?size="+str(size)+"&offset="+str(offset)
    response = requests.get(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    return info["payload"]

def get_jobinfo(jobid):
    headers = {
        "Content-Type": 'application/json',
        "Authorization": get_tocken()
    }
    url = "http://192.168.204.24/rest-server/api/v1/jobs/" + str(jobid)
    response = requests.get(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    return info

def creat_mission(job_name, command):
    url = f'http://192.168.204.24/rest-server/api/v1/jobs/{job_name}'

    print(url)
    data = \
        f"""
    {{
    "jobName": "{job_name}",
    "retryCount": 0,
    "gpuType": "dgx",
    "image": "dockerhub.pcl.ac.cn:5000/user-images/wudch:1.1",
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
        "Authorization": get_tocken()
    }
    response = requests.put(url=url, json=json.loads(data), headers=headers)
    info = bytes2dict(response)
    return info

def delete_job(jobid):
    headers = {
        "Content-Type": 'application/json',
        "Authorization": get_tocken()
    }
    url = "http://192.168.204.24/rest-server/api/v1/jobs/" + str(jobid)
    response = requests.delete(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    return info

if __name__ == "__main__":
    command = "cd ../userhome/network-pruning-rfm-master/cifar/l1-norm-pruning/&&PYTHONPATH=./ python main.py --dataset cifar10 --arch vgg --depth 16 --save './log/ori_vgg16'"
    #creat_mission("rua",command)
    a = get_joblist("wudch")
    print("a",a["jobs"][0])
    import time

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
    print(result[0])
    get_userinfo("wudch")
