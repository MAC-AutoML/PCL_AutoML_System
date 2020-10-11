from django.shortcuts import render
from django.shortcuts import redirect
from . import models

from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    pass
    return render(request, 'index.html')


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
            return redirect('/userinfo/')
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


def userinfo(request):

    return render(request, "userinfo.html")
