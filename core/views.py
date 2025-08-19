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
from rest_framework.request import Request
from TaskManagementAPI.helper import (
    dynamic_search
)
from TaskManagementAPI.pagination import (
    DynamicPagination
)
from rest_framework.views import APIView
from django.db.models import Q


# views
# users view
class UsersAPI(ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users.objects.all()
    pagination_class = DynamicPagination

    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(
                request=request, model=Users, serializer=UsersSerializer,
                pagination_class=DynamicPagination()
            )
        return super().list(request, *args, **kwargs)


# project views
class ProjectsAPI(
    GenericViewSet, ListModelMixin,
    CreateModelMixin, UpdateModelMixin,
    RetrieveModelMixin
):
    serializer_class = ProjectSerializer
    queryset = Projects.objects.all()
    pagination_class = DynamicPagination

    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(
                request=request, model=Projects, serializer=ProjectSerializer,
                pagination_class=DynamicPagination()
            )
        return super().list(request, *args, **kwargs)


# tasks view
class TasksAPI(ModelViewSet):
    serializer_class = TasksSerializer
    queryset = Tasks.objects.all()
    pagination_class = DynamicPagination

    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(
                request=request, model=Tasks, serializer=TasksSerializer,
                pagination_class=DynamicPagination()
            )
        return super().list(request, *args, **kwargs)


# paginator
paginator = DynamicPagination()


# tasks that the logged in manager added
class TasksManager(APIView):
    # permission_classes -> allow for logged in managers

    def get(self, request: Request):
        manager = request.user
        tasks = Tasks.objects.filter(Q(user=manager.id))
        paginated_tasks = paginator.paginate_queryset(tasks, request)
        return paginator.get_paginated_response(TasksSerializer(paginated_tasks, many=True).data)
