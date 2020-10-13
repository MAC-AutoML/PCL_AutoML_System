from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    _path = models.CharField(max_length=256, default='')

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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


# public algorithm class
class Algorithm(models.Model):
    name = models.CharField(max_length=128, unique=True)
    task = models.CharField(max_length=128)
    # code path
    _path = models.CharField(max_length=256, default='')
    is_check = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class User_algorithm(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, models.CASCADE)
    algorithm = models.ForeignKey(Algorithm, models.SET_NULL, null=True, blank=True)
    task = models.CharField(max_length=128, default='')
    _path = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class User_Job(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, models.CASCADE)
    algorithm = models.ForeignKey(User_algorithm, models.CASCADE)
    dataset = models.ForeignKey(Dataset, models.SET_NULL, null=True)
    _path = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
