"""AutoML_Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.conf.urls import url,include

from django.urls import path,re_path
from django.views.static import serve

from django.views.generic.base import TemplateView

from .settings import MEDIA_ROOT

import sys
sys.path.append("..")
from _app import views as app_views
from backend import views as back_views

urlpatterns = [
    # Manage tool urls
    path('admin/', admin.site.urls),
    url(r"^api-auth/", include("rest_framework.urls")),
    # new urls: backend
    path('backend/login/account', back_views.Login.as_view(), name='login'),
    re_path(r'^/backend/login/.*', back_views.Login.as_view(), name='login'),
    path('api/currentUser/', back_views.currentUser.as_view(), name='login'),

    # old urls: _app
    #path('', app_views.login,name='login'),
    url(r'^(algorithm|dataset)/?$',app_views.list_public,name="public"),
    url(r'^(algorithm|dataset)/([0-9]+)/?$',app_views.detail_public,name="detail_public"),
    url(r'^own/',include("_app.urls")),
    # url(r'index/',include("django_adminlte_theme.urls"),name='index'),
    # AutoML_Web/django_adminlte_theme/templates/admin/index.html
    path('mission_center/',app_views.mission_center,name='mission_center'),
    url(r'^deleting/([0-9a-zA-Z]+)/?$',app_views.delete_job,name='delete_job'),
    url(r'^media/(?P<path>.+)$', serve, {'document_root':MEDIA_ROOT}),
    
    path('login/', app_views.login, name='login'),
    path('index/', app_views.index,name='index'),
    path('register/', app_views.register,name='register'),
    path('logout/', app_views.logout,name='logout'),
    path('userinfo/',app_views.userinfo,name='userinfo'),
    path('set_password/',app_views.set_password,name='set_password'),
    re_path(r'^.*$', app_views.redirecter),
]
