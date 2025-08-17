from rest_framework.serializers import ModelSerializer
from action import models

# foreign serializers
from core.serializers import (
    UsersSerializer, TasksSerializer, ProjectSerializer
)


# tags serializers
class TagsSerializer(ModelSerializer):
    user_detail = UsersSerializer(source='user', read_only=True)
    task_detail = TasksSerializer(source='task', read_only=True)

    class Meta:
        model = models.Tags
        fields = '__all__'


# scores serializers
class ScoresSerializer(ModelSerializer):
    user_detail = UsersSerializer(source='user', read_only=True)
    task_detail = TasksSerializer(source='task', read_only=True)

    class Meta:
        model = models.Scores
        fields = '__all__'


# project members
class ProjectMembersSerializer(ModelSerializer):
    member_detail = UsersSerializer(source='member', read_only=True)
    project_detail = ProjectSerializer(source='project', read_only=True)

    class Meta:
        model = models.ProjectMembers
        fields = '__all__'
