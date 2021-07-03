from rest_framework import serializers
from _app.models import Algorithm,User_Job,User_algorithm,Dataset, customize_algo

class JobsSerializers(serializers.ModelSerializer):
    class Meta:
        model = User_Job  # 指定的模型类
        fields = ('jobid','name', 'username', 'state', 'createdTime','_path','algorithm_id')  # 需要序列化的属性

class AlgorithmSerializers(serializers.ModelSerializer):
    class Meta:
        model = Algorithm  # 指定的模型类
        fields = ('id', 'name', 'task', "_path", "is_check")  # 需要序列化的属性

class UAlgorithmSerializers(serializers.ModelSerializer):
    class Meta:
        model = User_algorithm  # 指定的模型类
        fields = ('id', 'name', 'task', "_path", "user_id", "algorithm_id")  # 需要序列化的属性

class DatasetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Dataset  # 指定的模型类
        fields = ('id', 'name', 'task', "_path", "is_check")  # 需要序列化的属性
class CAlgorithmSerializers(serializers.ModelSerializer):
    class Meta:
        model= customize_algo
        fields = ("id","name","description","created_at","edited_at","ai_engine","project_path","start_path",)


