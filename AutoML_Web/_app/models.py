from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    _path = models.CharField(max_length=256, default='')
    tocken = models.CharField(max_length=1024, default='')
    #mntpath = models.CharField(max_length=1024, default='')
    ## 不能直接把api传来的id赋值给数据库里的id，会有莫名的bug
    #api_id = models.BigIntegerField(unique=True, default=-1)
    
    def __str__(self):
        # return self.first_name + self.last_name
        return self.username

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ["-id"]

# public dataset class
class Dataset(models.Model):
    name = models.CharField(max_length=128, unique=True)
    task = models.CharField(max_length=128)
    _path = models.CharField(max_length=256, default='')
    is_check = models.BooleanField(default=False)
    objects=models.Manager()
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

# public algorithm class
class Algorithm(models.Model):
    name = models.CharField(max_length=128, unique=True)
    task = models.CharField(max_length=128)
    # code path
    _path = models.CharField(max_length=256, default='')
    is_check = models.BooleanField(default=False)
    objects=models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

class User_algorithm(models.Model):
    name = models.CharField(max_length=128)
    user_id = models.IntegerField()
    algorithm = models.ForeignKey(Algorithm, models.SET_NULL, null=True, blank=True)
    task = models.CharField(max_length=128, default='')
    _path = models.CharField(max_length=256, default='')
    objects=models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

class User_Job(models.Model):
    jobid = models.CharField(max_length=128,unique=True)
    name = models.CharField(max_length=128)
    user_id = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    createdTime = models.CharField(max_length=128)
    completedTime = models.CharField(max_length=128)
    algorithm = models.ForeignKey(User_algorithm, models.CASCADE)
    dataset = models.ForeignKey(Dataset, models.SET_NULL, null=True)
    _path = models.CharField(max_length=256, default='')
    objects=models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]