from django.shortcuts import render
from django.shortcuts import redirect
from . import models

# Create your views here.


def index(request):
    pass
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        message = '请检查填写的内容！'
        if username.strip() and password:
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(name=username)
            except Exception:
                message = '用户不存在！'
                return render(request, 'login.html', {'message': message})

            if user.password == password:
                print(username, password)
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login.html', {'message': message})
        else:
            return render(request, 'login.html', {'message': message})
    return render(request, 'login.html')


def register(request):
    pass
    return render(request, 'register.html')


def logout(request):
    pass
    return redirect("/login/")
