from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from django.http import HttpResponse


from . import models

from django.core.paginator import Paginator

from django.contrib import auth
from django.contrib.auth.decorators import login_required
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
                pub=PRIVATE_DICT[name].all().filter(user=request.user)
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
    user=request.user
    content={}
    if(int(pk)==0):
        # return redirecter(request)
        return render(request,"manage.html",content)
    item=None
    if(PRIVATE_DICT.__contains__(typer)):
        item=PRIVATE_DICT[typer].filter(user=user).filter(id=pk)[0]
    content["item"]=item
    if(request.method == "GET"):
        return render(request,"page.html",content)
    if(request.method == 'POST'): # Ready for Form POST methods
        item=None
        # return redirect(reverse("detail_private",args=(typer,item.id)))
        return redirect(reverse("private",args=(typer,)))

@login_required
def edit_job(request,task):
    # 需要添加对task的格式检查功能？
    user=request.user
    content={}
    task=str(task)
    task=task.strip(" ").replace("_"," ")# 现有的分类任务名为 "Image Classification"
    content['task']=str(task)
    # 使用task类型来限定下拉列表数据集种类和下拉私有算法种类
    if(request.method == "GET"):
        #查询数据库
        content['dataset']=models.Dataset.objects.filter(task=task).order_by("id")
        content['algorithm']=models.User_algorithm.objects.filter(user=user).filter(task=task).order_by("id")

        if(len(content['dataset']) ==0 or len(content['algorithm'])==0):
        # 说明没有对应的任务或数据集
            return redirect(reverse("mission_center"))        
    #表单回传,用关键字填充发给云脑的命令
    elif(request.method == "POST"):
        print(request.POST)
        return redirect(reverse("mission_center")) 
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

@login_required
def mission_center(request):
    user=request.user
    content={}
    pass
    return render(request,"mission_center.html",content)