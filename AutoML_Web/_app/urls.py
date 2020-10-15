
from django.urls import path,re_path
from django.conf.urls import url,include
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'([0-9]*)/?$',TemplateView.as_view(template_name="test.html")),
]