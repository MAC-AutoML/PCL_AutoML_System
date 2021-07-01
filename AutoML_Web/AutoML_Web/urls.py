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

from backend import views

# Debug用
if(__name__=='__main__'):
    from ..backend import views

urlpatterns = [
    # Manage tool urls
    path('admin/', admin.site.urls),
    url(r"api-auth/", include("rest_framework.urls"),name='api_check'),
    url(r'api/login/account', views.Login.as_view(), name='log'),
    url(r'api/currentUser', views.CurrentUser.as_view(), name='current'),
    url(r'api/automl',views.AutoML.as_view(),name='automl'),
    url(r'api/AImarket',views.AIMarket.as_view(),name='aimarket'),
    url(r'api/algoManage',views.AlgoManage.as_view(),name='algo_manage'),
    
    url(r'api/refresh/dataset',views.RefreshData.as_view(),name='refresh_dataset'),
    url(r'api/refresh/path',views.RefreshPath.as_view(),name='refresh_path'),

]
