from rest_framework.serializers import ModelSerializer, CharField
from core import models


# user serializers
class UsersSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = models.Users
        fields = '__all__'


# project serializers
class ProjectSerializer(ModelSerializer):
    user_detail = UsersSerializer(source='user', read_only=True)

    class Meta:
        model = models.Projects
        fields = '__all__'


# task serializers
class TasksSerializer(ModelSerializer):
    user_detail = UsersSerializer(source='user', read_only=True)
    project_detail = ProjectSerializer(source='project', read_only=True)
    foreman_detail = UsersSerializer(source='foreman', read_only=True)

    class Meta:
        model = models.Tasks
        fields = '__all__'
