from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin
)
from .serializers import (
    UsersSerializer, ProjectSerializer, TasksSerializer
)
from .models import (
    Users, Projects, Tasks
)


# views
# users view
class UsersAPI(ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users.objects.all()


# project views
class ProjectsAPI(
    GenericViewSet, ListModelMixin,
    CreateModelMixin, UpdateModelMixin,
    RetrieveModelMixin
):
    serializer_class = ProjectSerializer
    queryset = Projects.objects.all()


# tasks view
class TasksAPI(ModelViewSet):
    serializer_class = TasksSerializer
    queryset = Tasks.objects.all()
