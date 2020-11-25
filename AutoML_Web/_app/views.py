from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.db import connection
from django.http import HttpResponse
from django.http import JsonResponse

from . import models

from django.core.paginator import Paginator

from django.contrib import auth
from django.contrib.auth.decorators import login_required
import tools.API_tools as API_tools
from  tools.API_tools import get_keyword
import time

from .mock import USER_LIST,get_tocken
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
@login_required
def index(request):
    user = request.user
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

        ### Dev mock user   
        message = '请检查填写的内容！'
        index=-1
        for (i,item) in enumerate(USER_LIST):
            name=item['username']
            pw=item['password']
            if(username==name and password==pw):
                index=i
        if(index<0):
            message = "用户名或密码错误！"
            print(message)
            return render(request, 'login.html', {'message': message})
        else:
            #检查并创建数据库用户了
            UID = USER_LIST[index]['id']
            DUser = models.User.objects.filter(id = UID)
            print("输出一部分信息：",UID,DUser)
            if len(DUser) == 0:
                new_user = models.User.objects.create_user(
                    username=USER_LIST[index]['username'],
                    tocken = USER_LIST[index]['tocken'],
                    password=USER_LIST[index]['password'],
                    first_name = USER_LIST[index]['first_name'],
                    api_id = USER_LIST[index]['id'])
                ## 不能直接把api传来的id赋值给数据库里的id，会有莫名的bug
                new_user.save()
            else:
                DUser[0].username = username
                DUser[0].set_password(password)
                DUser[0].first_name = password
                DUser[0].tocken = get_tocken()
                DUser[0].save()
            user = auth.authenticate(
                username=username, password=password)  # 验证是否存在用户
            print(user)
            if (user):
                print("login!!!!!!!!!!!!!!!!!!")
                auth.login(request, user)
                return redirect('/index/')
            return redirect('/index/')            
        ### Raw user
        # message = '请检查填写的内容！'
        # uinfo = API_tools.check_user(username,password)  # 验证是否存在用户
        # if "错误" in uinfo:
        #     message = "用户名或密码错误！"
        #     return render(request, 'login.html', {'message': message})
        # else:
        #     #检查并创建数据库用户了
        #     UID = uinfo["payload"]["userInfo"]["userId"]
        #     DUser = models.User.objects.filter(id = UID)
        #     print(UID,DUser)
        #     if len(DUser) == 0:
        #         new_user = models.User.objects.create_user(
        #             username=username,
        #             tocken = API_tools.get_tocken(username,password),
        #             password=password,
        #             first_name = password,
        #             id = UID)
        #         new_user.save()
        #     else:
        #         DUser[0].username = username
        #         DUser[0].set_password(password)
        #         DUser[0].first_name = password
        #         DUser[0].tocken = API_tools.get_tocken(username,password)
        #         DUser[0].save()
        #     user = auth.authenticate(
        #         username=username, password=password)  # 验证是否存在用户
        #     print(user)
        #     if (user):
        #         print("login!!!!!!!!!!!!!!!!!!")
        #         auth.login(request, user)
        #         return redirect('/index/')
        #     #request.session["username"] = username
        #     #request.session["password"] = password
        #     #request.session["uid"] = uinfo["payload"]["userInfo"]["userId"]
        #     return redirect('/index/')
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
    user = request.user
    content=list_getter(typer,PUBLIC_DICT)
    content["list"]=content["list"].all()
    content["is_public"]=True

    return render(request,"pub_list.html",content)

@login_required
def list_private(request,typer):
    user = request.user
    content = {}
    content["type"] = typer
    if typer == "algorithm":
        DUser = models.User.objects.filter(id=user.id)
        content["list"]=models.User_algorithm.objects.filter(user_id=user.id)
        print(content["list"])
    elif typer == "job":
        content["list"] = models.User_Job.objects.filter(user_id=user.id)
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
    item = None
    if (PUBLIC_DICT.__contains__(typer)):
        item = PRIVATE_DICT[typer].filter(id=pk)[0]
    content["item"] = item
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
    item = models.User_Job.objects.filter(jobid=pk)[0]
    content["item"] = item
    if (request.method == "GET"):
        return render(request, "page.html", content)
    if (request.method == 'POST'):  # Ready for Form POST methods
        item = None
        # return redirect(reverse("detail_private",args=(typer,item.id)))
        return redirect(reverse("mission_center", args=(typer,)))



@login_required
def edit_classifyjob(request,task):
    user = request.user
    updata_user_algorithm(user.username,user.id)
    content={}
    # task=str(task)
    task=str(task).strip(" ").replace(" ","_")# 现有的分类任务名为 "Image Classification"
    content['task']=task
    # 使用task类型来限定下拉列表数据集种类和下拉私有算法种类
    if(request.method == "GET"):
        #查询数据库
        content['dataset']=models.Dataset.objects.filter(task=task).order_by("id")
        # # 【临时改动】
        # content['dataset']=models.Dataset.objects.all().order_by("id")
        #content['user_algorithm']=models.User_algorithm.objects.filter(task=task).order_by("id")
        # ds = request.GET.get('data_select')
        # # 【临时改动】
        # content['user_algorithm'] = ['272', '769', '855']

        content['user_algorithm'] = ['272', '769', '855', '1730']

        if(len(content['dataset']) ==0 or len(content['user_algorithm'])==0):# 说明没有对应的任务或数据集
            return redirect(reverse("mission_center"))        
    #表单回传,用关键字填充发给云脑的命令
    elif(request.method == "POST"):
        data_selectname = models.Dataset.objects.filter(id=str(request.POST["data_select"]))[0].name
        algo_select = "resnet20"#resnet20,densenet,resnet50,resnet110
        a_index = request.POST["algo_select"]
        bound = [300, 800]
        if "cifar" in data_selectname:
            dict_algo_select_name = ["resnet20", "densenet", "resnet50", "resnet110"]
            FLOPS_c = ['272', '769', '855', '1730']
            accept_index = FLOPS_c.index(a_index)
            #for index,i in enumerate(FLOPS_c):
            #    if i < bound[1] and i > bound[0]:
            #        accept_index = index
            algo_select = dict_algo_select_name[accept_index]
        if "image" in data_selectname:
            algo_select_name = ["resnet18", "densenet","resnet"]
            FLOPS_i = ['272', '769', '855', '1730']
            accept_index = FLOPS_i.index(a_index)
            #for index,i in enumerate(FLOPS_i):
            #    if i < bound[1] and i > bound[0]:
            #        accept_index = index
            algo_select = algo_select_name[accept_index]
        #print("data_select", request.POST["cost_bound"])
        algo_selectname = algo_select
        
        #print(algo_selectname,data_selectname)
        command = "cd ../userhome;mkdir jobspace;cd jobspace;mkdir classification;cd classification;mkdir algorithm;cd algorithm;"
        command = command+"cp -r -f /userhome/PCL_AutoML/PCL_AutoML_System/algorithm/classification/pytorch_image_classification ./;"
        outputdir = str(request.POST['job_name'])+"_"+str(data_selectname)+"_"+str(algo_selectname)+"_exp_"+str(time.time())
        #command = command+"mkdir "+outputdir+";"
        command = command+"cd pytorch_image_classification;"
        if "cifar" in str(data_selectname):
            command = command+"PYTHONPATH=./ python train.py --config configs/cifar/"+str(algo_selectname)+".yaml"
        if "imagenet" in str(data_selectname):
            command = command+"PYTHONPATH=./ python train.py --config configs/imagenet/"+str(algo_selectname)+".yaml"

        command = command+" train.output_dir /userhome/jobspace/classification/" + outputdir
        command = command+" dataset.name " + str(data_selectname).upper()
        '''
        if request.POST["lr"]:
            command = command+" train.base_lr " + str(request.POST["lr"])
        if request.POST["epoch"]:
            command = command+" scheduler.epochs "+ str(request.POST["epoch"])'''
        print(command)
        print("algo_select",algo_select)
        info = API_tools.creat_mission(str(request.POST['job_name']),command,user.tocken,user,user.first_name)
        timeArray = time.localtime()
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        if not info["payload"]:
            print("error~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return redirect(reverse("mission_center"))
        jobid = get_keyword(str(info["payload"]["jobId"]))
        name = get_keyword(str(request.POST['job_name']))
        username = get_keyword(str(user.username))
        user_id = str(user.id)
        state = get_keyword("WAITTING")
        createdTime = get_keyword(str(otherStyleTime))
        completedTime = get_keyword(str(0))
        _path = get_keyword(str("/userhome/jobspace/classification/"+outputdir))
        Da = models.User_algorithm.objects.filter(user_id=user.id).filter(name = algo_select)[0]
        algorithm_id = get_keyword(str(Da.id))
        dataset_id = get_keyword(str(request.POST["data_select"]))
        with connection.cursor() as cursor:
            sqltext = "INSERT INTO `automl_web`.`_app_user_job`(`jobid`, `name`, `username`, `user_id`, `state`, `createdTime`, `completedTime`,`_path`, `algorithm_id`, `dataset_id`) " \
                      "VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}','{9}');".format(
                jobid,name,username,user_id,state,createdTime,completedTime,_path,algorithm_id,dataset_id
            )
            print("$$$$$$$$$$$",sqltext)
            cursor.execute(sqltext)
        return redirecter(request, dst="/mission_center/")
    print("Content is: ",content)
    return render(request,"manage_job.html",content)

def refresh_modelsize(request):
    print("Yes")
    test_group=[
        [100,200,300,400],
        [101,201,301,401],
        [102,202,302,402],
        [103,203,303,403]
    ]
    model_id=request.GET.get('mid')
    slist=test_group[int(model_id)]
    return JsonResponse({'slist':slist})
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
    for it in pk:
        print("it",it)
        if it not in fk:
            palobj = models.Algorithm.objects.filter(id=it)[0]
            ujb = models.User_algorithm.objects.create(algorithm_id = it,user_id=uid,name=palobj.name,task=palobj.task,_path=palobj._path)
            ujb.save()

@login_required
def mission_center(request):
    print(request.method)
    if request.method == "GET":
        #print(request.GET["ipt"])
        is_search = False
        try:
            print(request.GET["ipt"])
        except:
            is_search = False
        else:
            is_search = True
        print(is_search)
        user=request.user
        updata_jobtable(user.tocken,user,user.first_name)
        content={}
        joblist = models.User_Job.objects.all().filter(username=user).order_by("algorithm_id")
        if is_search:
            joblist = joblist.filter(name__contains=request.GET["ipt"]).order_by("algorithm_id")
        l_algorithm_id = []
        for jb in joblist:
            if jb.algorithm_id not in l_algorithm_id:
                l_algorithm_id.append(jb.algorithm_id)
        print(l_algorithm_id)
        algorithm_name = []
        algorithm_joblist = []
        #按照算法外键进行分类
        for i,l in enumerate(l_algorithm_id):
            algorithm_name.append(models.User_algorithm.objects.all().filter(id=l)[0].name)
            tm = models.User_Job.objects.all().filter(username=user).filter(algorithm_id=l).order_by("id")
            if is_search:
                tm = tm.filter(name__contains=request.GET["ipt"]).order_by("id")
            tt = {}
            tt["al_name"] = algorithm_name[i]
            tt["joblist"] = tm.values('jobid','name','username','state','createdTime','_path').order_by("createdTime").reverse()
            for tte in tt["joblist"]:
                tte['path'] = tte.pop('_path')
            algorithm_joblist.append(tt)
        content["algorithm_joblist"] = algorithm_joblist
        return render(request,"mission_center.html",content)
    if request.method == "POST":
        print("POST")

@login_required
def delete_job(request,jobid):
    user = request.user
    content = {}
    print("????????????????????????????$DELETEING")
    API_tools.delete_job(jobid,user.tocken,user,user.first_name)
    return redirecter(request, dst="/mission_center/")