
from django.urls import path,re_path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('index/',TemplateView.as_view(template_name="admin/testers.html")),
]
