from rest_framework import serializers
from _app.models import Algorithm,User_Job

class JobsSerializers(serializers.ModelSerializer):
    class Meta:
        model = User_Job  # 指定的模型类
        fields = ('jobid','name', 'username', 'state', 'createdTime','_path','algorithm_id')  # 需要序列化的属性

class AlgorithmSerializers(serializers.ModelSerializer):
    class Meta:
        model = Algorithm  # 指定的模型类
        fields = ('pk', 'name', 'task', )  # 需要序列化的属性




