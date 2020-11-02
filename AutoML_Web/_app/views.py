from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.db import connection
from django.http import HttpResponse


from . import models

from django.core.paginator import Paginator

from django.contrib import auth
from django.contrib.auth.decorators import login_required
import tools.API_tools as API_tools
from  tools.API_tools import get_keyword
import time

# Create your views here.
TOP=5
PUBLIC_DICT={
    "algorithm":models.Algorithm.objects,
    "dataset":models.Dataset.objects,
}
PRIVATE_DICT={
    "algorithm":models.User_algorithm.objects,
    "job":models.User_Job.objects,
}
KEYS={
    "public":["algorithm","dataset"],
    "private":["algorithm","job"],
}
def list_getter(typer,dicts):
    content={}
    content["type"]=typer
    lister=None

    if(dicts.__contains__(typer)):
        lister=dicts[typer]
    content["list"]=lister
    return content

def redirecter(request,dst:str="/index/"):
    return redirect(dst)

def index(request):
    content={}
    content["public"]={}
    content["private"]={}
    for name in KEYS["public"]:
        pub=PUBLIC_DICT[name].all().order_by('id')
        pub=pub[:TOP if TOP<pub.count() else pub.count()]
        pub_name=[ [item.name,item.id] for item in pub]
        content["public"][name]=pub_name
    if(request.user):
        if(request.user.is_staff):
            return redirecter(request,"/admin/")
        if(request.user.is_authenticated):
            for name in KEYS["private"]:
                pub=PRIVATE_DICT[name].all().filter()
                pub=pub[:TOP if TOP<pub.count() else pub.count()]
                pub_name=[ [item.name,item.id] for item in pub]
                content["private"][name]=pub_name
            pass
    return render(request, 'index.html',content)

def login(request):
    if(request.method == "GET"):
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # valid_num = request.POST.get("valid_num")
        # keep_str = request.session.get("keep_str")
        message = '请检查填写的内容！'
        user = auth.authenticate(
            username=username, password=password)  # 验证是否存在用户
        if(user):
            auth.login(request, user)
            return redirect('/index/')
        else:
            message = "用户名或密码错误！"
            return render(request, 'login.html', {'message': message})
    return render(request, 'login.html')


def register(request):
    if(request.method == "GET"):
        return render(request, 'register.html')
    elif(request.method == "POST"):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        email = request.POST.get('email', '')
        if(models.User.objects.filter(username=username) or username == '0'):
            content = {
                'username': username
            }
            return render(request, 'register.html', content)
        elif(password == repeat_password):
            new_user = models.User.objects.create_user(username=username,
                                                       password=password, email=email)
            new_user.save()
            return redirect('/index/')
        pass


@login_required
def set_password(request):
    iuser = request.user
    state = None
    if(request.method == "GET"):
        return render(request, 'set_password.html')
    if(request.method == 'POST'):
        old_p = request.POST.get('old_password', '')
        new_p = request.POST.get('new_password', '')
        rep_p = request.POST.get('repeat_password', '')
        if(iuser.check_password(old_p)):
            if(not new_p):
                state = 'empty'
            elif(new_p != rep_p):
                state = 'not the same password'
            else:
                iuser.set_password(new_p)
                iuser.save()
                return redirect('/userinfo/')
        content = {
            'user': iuser,
            'state': state
        }
        return render(request, 'set_password.html', content)

def logout(request):
    auth.logout(request)
    return redirect("/login/")

@login_required # Waited
def userinfo(request):
    return render(request, "userinfo.html")

def list_public(request,typer):
    content=list_getter(typer,PUBLIC_DICT)
    content["list"]=content["list"].all()
    content["is_public"]=True

    return render(request,"pub_list.html",content)

@login_required
def list_private(request,typer):
    user=request.user
    content=list_getter(typer,PRIVATE_DICT)
    content["list"]=content["list"].filter(user=user)
    return render(request,"pub_list.html",content)

def detail_public(request,typer,pk):
    content={}
    item=None
    if(PUBLIC_DICT.__contains__(typer)):
        item=PUBLIC_DICT[typer].filter(id=pk)[0]    
    content["item"]=item
    content["path"]=item._path
    return render(request,"page.html",content)

@login_required
def detail_private(request,typer,pk):
    # 自增的id从1开始，因此假设id(pk)为0时是要增加算法/作业
    user = request.user
    content = {}
    print(pk, request.method)
    joblist = API_tools.get_jobinfo(pk)
    content["item"] = joblist
    for key in content["item"]:
        print(key, content["item"][key])
    if (request.method == "GET"):
        return render(request, "page.html", content)
    if (request.method == 'POST'):  # Ready for Form POST methods
        item = None
        # return redirect(reverse("detail_private",args=(typer,item.id)))
        return redirect(reverse("private", args=(typer,)))

@login_required
def detail_job(request,typer,pk):
    user = request.user
    content = {}
    print(pk, request.method)
    jobdt = API_tools.get_jobinfo(pk)
    content["item"] = jobdt["payload"]["jobStatus"]
    for key in content["item"]:
        print(key, content["item"][key])
    if (request.method == "GET"):
        return render(request, "page.html", content)
    if (request.method == 'POST'):  # Ready for Form POST methods
        item = None
        # return redirect(reverse("detail_private",args=(typer,item.id)))
        return redirect(reverse("mission_center", args=(typer,)))



@login_required
def edit_classifyjob(request,task):
    user = request.user
    updata_user_algorithm(user)
    content={}
    task=str(task)
    task=task.strip(" ").replace("_"," ")# 现有的分类任务名为 "Image Classification"
    content['task']=str(task)
    print(request.method)
    # 使用task类型来限定下拉列表数据集种类和下拉私有算法种类
    if(request.method == "GET"):
        #查询数据库
        content['dataset']=models.Dataset.objects.filter(task=task).order_by("id")
        content['user_algorithm']=models.User_algorithm.objects.filter(task=task).order_by("id")
        print("####",content['user_algorithm'])
        print(len(content['dataset']) ==0 or len(content['user_algorithm'])==0)
        #content['algorithm'] = models.Algorithm.objects.filter().filter(task=task).order_by("id")
        if(len(content['dataset']) ==0 or len(content['user_algorithm'])==0):
        # 说明没有对应的任务或数据集
            return redirect(reverse("mission_center"))        
    #表单回传,用关键字填充发给云脑的命令
    elif(request.method == "POST"):
        algo_selectname = models.User_algorithm.objects.filter(id=str(request.POST["algo_select"]))[0].name
        data_selectname = models.Dataset.objects.filter(id=str(request.POST["data_select"]))[0].name
        #print(algo_selectname,data_selectname)
        command = "cd ../userhome/PCL_AutoML/jobspace;mkdir classification;cd classification;"
        outputdir = str(request.POST['job_name'])+"_"+str(data_selectname)+"_"+str(algo_selectname)+"_exp_"+str(time.time())
        command = command+"mkdir "+outputdir+";"
        command = command+"cd ..;cd ../algorithms/classification/pytorch_image_classification;"
        if "cifar" in str(data_selectname):
            command = command+"PYTHONPATH=./ python train.py --config configs/cifar/"+str(algo_selectname)+".yaml"
        command = command+" train.output_dir " + outputdir
        if request.POST["lr"]:
            command = command+" train.base_lr " + str(request.POST["lr"])
        if request.POST["epoch"]:
            command = command+" scheduler.epochs "+ str(request.POST["epoch"])
        print(command)
        info = API_tools.creat_mission(str(request.POST['job_name']),command)
        timeArray = time.localtime()
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        jobid = get_keyword(str(info["payload"]["jobId"]))
        name = get_keyword(str(request.POST['job_name']))
        username = get_keyword(str(user))
        uinfo = API_tools.get_userinfo(str(user))
        user_id = str(uinfo["payload"]["userInfo"]["uid"])
        state = get_keyword("WAITTING")
        createdTime = get_keyword(str(otherStyleTime))
        completedTime = get_keyword(str(0))
        _path = get_keyword(str(outputdir))
        algorithm_id = get_keyword(str(request.POST["algo_select"]))
        dataset_id = get_keyword(str(request.POST["data_select"]))
        with connection.cursor() as cursor:
            sqltext = "INSERT INTO `automl_web`.`_app_user_job`(`jobid`, `name`, `username`, `user_id`, `state`, `createdTime`, `completedTime`,`_path`, `algorithm_id`, `dataset_id`) " \
                      "VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}','{9}');".format(
                jobid,name,username,user_id,state,createdTime,completedTime,_path,algorithm_id,dataset_id
            )
            print("$$$$$$$$$$$",sqltext)
            cursor.execute(sqltext)
        return redirect(reverse("mission_center"))
    print(content)
    return render(request,"manage_job.html",content)
@login_required
def edit_algorithm(request,task):
    user=request.user
    content={}
    pass
    return redirecter(request,dst="/mission_center/")
    # return render(request,"manage.html",content)    
@login_required    
def item_edit(request,typer,pk,task):
    user=request.user
    content={}
    pass
    return redirecter(request,dst="/mission_center/")
    # return render(request,"manage.html",content)

def updata_jobtable():
    job = models.User_Job.objects.all().order_by("id")
    job = job.exclude(state="STOPPED").exclude(state="FAIL").exclude(state="SUCCEEDED")
    for jd in job:
        jd_detail = API_tools.get_jobinfo(jd.jobid)
        jd.state = jd_detail["payload"]["jobStatus"]["state"]
        timeStamp2 = int(jd_detail['payload']['jobStatus']["completedTime"])
        if timeStamp2 != 0:
            timeArray2 = time.localtime(timeStamp2 / 1000)
            otherStyleTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray2)
            jd.completedTime = otherStyleTime2
        jd.save()

def updata_user_algorithm(user):
    u_alg = models.User_algorithm.objects.exclude(algorithm_id=None)
    p_alg = models.Algorithm.objects.all()
    uid = models.User.objects.filter(username=str(user))[0].id
    fk = []
    pk = []
    for it in u_alg:
        fk.append(it.algorithm_id)
    for it in p_alg:
        pk.append(it.id)
    for it in pk:
        print("it",it)
        if it not in fk:
            palobj = models.Algorithm.objects.filter(id=it)[0]
            ujb = models.User_algorithm.objects.create(algorithm_id = it,user_id=uid,name=palobj.name,task=palobj.task,_path=palobj._path)
            ujb.save()

@login_required
def mission_center(request):
    user=request.user
    updata_jobtable()
    content={}
    joblist = models.User_Job.objects.all().filter(username=user).order_by("algorithm_id")
    l_algorithm_id = []
    for jb in joblist:
        if jb.algorithm_id not in l_algorithm_id:
            l_algorithm_id.append(jb.algorithm_id)

    algorithm_name = []
    algorithm_joblist = []
    for i,l in enumerate(l_algorithm_id):
        algorithm_name.append(models.User_algorithm.objects.all().filter(id=l)[0].name)
        tm = models.User_Job.objects.all().filter(username=user).filter(algorithm_id=l).order_by("id")
        tt = {}
        tt["al_name"] = algorithm_name[i]
        tt["joblist"] = tm.values('jobid','name','username','state','createdTime','_path').order_by("createdTime").reverse()
        for tte in tt["joblist"]:
            tte['path'] = "/userhome/PCL_AutoML/jobspace/"+tte.pop('_path')
        algorithm_joblist.append(tt)
    content["algorithm_joblist"] = algorithm_joblist
    return render(request,"mission_center.html",content)

@login_required
def delete_job(request,jobid):
    user = request.user
    content = {}
    API_tools.delete_job(jobid)
    return redirecter(request, dst="/mission_center/")