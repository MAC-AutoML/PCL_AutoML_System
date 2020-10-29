from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.User)
admin.site.register(models.Dataset)
admin.site.register(models.Algorithm)
admin.site.register(models.User_algorithm)
admin.site.register(models.User_Job)
