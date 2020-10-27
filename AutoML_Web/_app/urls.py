
from django.urls import path,re_path
from django.conf.urls import url,include
from django.views.generic.base import TemplateView
from . import views
urlpatterns = [
    url(r'^(algorithm|job)/?$',views.list_private,name="private"),
    # 自增的id从1开始，因此假设id为0时是要增加算法/作业
    # url(r'^(algorithm|job)/(0)/?$',views.item_edit,name="manage"),
    # url(r'^(algorithm|job)/(0)/(?P<task>[a-zA-Z_]+)/$$',views.item_edit,name="manage"),
    url(r'^job/0/(?P<task>[a-zA-Z_]+)/?$',views.edit_job,name="manage_job"),
    url(r'^algorithm/0/(?P<task>[a-zA-Z_]+)/?$',views.edit_algorithm,name="manage_algorithm"),

    url(r'^(algorithm|job)/([0-9]+)/?$',views.detail_private,name="detail_private"),
    url(r'.*$',views.redirecter),
]