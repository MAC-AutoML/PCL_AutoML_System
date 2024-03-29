from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
# Create your models here.
# 模型写在这里是历史遗留问题

class User(AbstractUser):
    _path = models.CharField(max_length=256, default='')
    tocken = models.CharField(max_length=1024, default='')
    mntpath = models.CharField(max_length=1024, default='')
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
    created_at = models.CharField(max_length=256, default='')
    hyperp_path = models.CharField(max_length=256, default='')
    uid = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)

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
    created_at = models.CharField(max_length=256, default='')
    hyperp_path = models.CharField(max_length=256, default='')
    uid = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)

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
    
# # 算法创建部分
class customize_algo(models.Model):
    name=models.CharField(max_length=128, verbose_name="算法名称")
    version=models.CharField(max_length=128,blank=True, verbose_name="版本")
    description=models.TextField(verbose_name="算法描述", blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    edited_at=models.DateTimeField(auto_now=True)
    # 是 Python 的 DateTime 对象                                          
    ai_engine=models.CharField(max_length=128)
    project_path=models.CharField(max_length=256)
    start_path=models.CharField(max_length=256)
    code_path=models.CharField(max_length=256)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name
    class Meta:
        ordering= ["-id"]
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

class algo_hpyer(models.Model):
    name=models.CharField(max_length=128)
    # created_at=models.DateTimeField(auto_now_add=True) 
    # edited_at=models.DateTimeField(auto_now=True)                                          

    data_type=models.CharField(max_length=64) # options
    # https://docs.djangoproject.com/en/3.2/ref/models/fields/
    initial_value=models.CharField(max_length=256, blank=True)
    limitations=models.TextField(verbose_name="Json字符串形式保存的超参限制条件",
                                 blank=True) # 将参数的限制范围以json字符串的形式存储，
    is_necessary=models.BooleanField(default=False)
    description=models.TextField(verbose_name="描述", blank=True)
    belong_algo=models.ForeignKey(customize_algo,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name
    class Meta:
        ordering= ["-id"]
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

class algo_io(models.Model):
    fname=models.CharField(max_length=128)
    name=models.CharField(max_length=128)
    # created_at=models.DateTimeField(auto_now_add=True) 
    # edited_at=models.DateTimeField(auto_now=True)                                          

    default_path=models.CharField(max_length=256, blank=True)
    description=models.TextField(verbose_name="描述", blank=True)
    belong_algo=models.ForeignKey(customize_algo,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    class Meta:
        ordering= ["-id"]
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]    
class base_job(models.Model):
    job_id = models.CharField(max_length=128,unique=True)
    name = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    created_at = models.DateTimeField()
    completed_at=models.DateTimeField(blank=True,null=True)
    class Meta:
        abstract = True    
# # 创建训练作业部分
class customize_job(base_job):
    algo_id = models.ForeignKey(customize_algo,on_delete=models.SET_NULL,blank=True,null=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields] 
    
class customize_auto_search(models.Model):
    # 通用字段
    name = models.CharField(max_length=128)
    created_at=models.DateTimeField(auto_now_add=True)
    completed_at=models.DateTimeField(blank=True,null=True)
    state = models.CharField(max_length=128)

    # 外键 - 用户 算法
    algo_id = models.ForeignKey(customize_algo,on_delete=models.SET_NULL,blank=True,null=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    # 搜索字段
    method=models.CharField(max_length=64)
    suggest=models.IntegerField() # 一次给出建议的数量
    epoch=models.IntegerField()
    result=models.CharField(max_length=512,default="./result.txt")
    # 进程控制
    pid=models.IntegerField()
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields] 

class search_para(models.Model):
    # 通用字段
    # space - range 指定一个连续/离散的集合
    # values 指定一个离散的集合, 以空格分隔可能值的字符串
    # 这两个互斥 哪个不为空 这个参数就以哪个的形式来
    name = models.CharField(max_length=128)
    data_type=models.CharField(max_length=64) # options
    space=models.CharField(max_length=64,blank=True,null=True)
    values=models.TextField(max_length=2048,blank=True,null=True)
    ranges_max=models.CharField(max_length=64,blank=True,null=True)
    ranges_min=models.CharField(max_length=64,blank=True,null=True)
    
    search_id = models.ForeignKey(customize_auto_search, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields] 
    
class search_job(base_job):
    search_id = models.ForeignKey(customize_auto_search, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields] 
    