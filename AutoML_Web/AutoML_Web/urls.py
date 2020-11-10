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

from _app import views



urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.login,name='login'),
    url(r'^(algorithm|dataset)/?$',views.list_public,name="public"),
    url(r'^(algorithm|dataset)/([0-9]+)/?$',views.detail_public,name="detail_public"),
    url(r'^own/',include("_app.urls")),
    # url(r'index/',include("django_adminlte_theme.urls"),name='index'),
    # AutoML_Web/django_adminlte_theme/templates/admin/index.html
    path('mission_center/',views.mission_center,name='mission_center'),
    url(r'^deleting/([0-9a-zA-Z]+)/?$',views.delete_job,name='delete_job'),
    url(r'^media/(?P<path>.+)$', serve, {'document_root':MEDIA_ROOT}),
    path('login/', views.login, name='login'),
    path('index/', views.index,name='index'),
    path('register/', views.register,name='register'),
    path('logout/', views.logout,name='logout'),
    path('userinfo/',views.userinfo,name='userinfo'),
    path('set_password/',views.set_password,name='set_password'),
    re_path(r'^.*$', views.redirecter),
]
