from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)
    _path = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]


# public dataset class
class Dataset(models.Model):
    name = models.CharField(max_length=128, unique=True)
    task = models.CharField(max_length=128)
    _path = models.CharField(max_length=256, default='')
    is_check = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]


# public algorithm class
class Algorithm(models.Model):
    name = models.CharField(max_length=128, unique=True)
    task = models.CharField(max_length=128)
    # code path
    _path = models.CharField(max_length=256, default='')
    is_check = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]


class User_algorithm(models.Model):
    name = models.CharField(max_length=128)
    user_id = models.CharField(max_length=128, default='')
    _path = models.CharField(max_length=256, default='')


class User_Job(models.Model):
    job_name = models.CharField(max_length=128)
    task = models.CharField(max_length=128)
    dataset_name = models.CharField(max_length=128)
    _path = models.CharField(max_length=256, default='')
