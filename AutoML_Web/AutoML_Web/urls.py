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
from backend import views

urlpatterns = [
    # Manage tool urls
    path('admin/', admin.site.urls),
    url(r"^api-auth/", include("rest_framework.urls")),
    url(r'api/login/account', views.Login.as_view(), name='login'),
    url(r'api/currentUser', views.currentUser.as_view(), name='current'),

]
