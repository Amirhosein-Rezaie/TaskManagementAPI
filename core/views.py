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
from action.models import (
    Tags, ProjectMembers
)


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


# tasks that is for specific project
class TasksProject(APIView):
    # permission_classes -> for logged in users

    def get(self, request: Request, project_id: int):
        tasks = Tasks.objects.filter(Q(project=project_id))
        paginated_tasks = paginator.paginate_queryset(tasks, request)
        return paginator.get_paginated_response(TasksSerializer(paginated_tasks, many=True).data)


# tasks that is picked by a specific foreman
class TasksForeman(APIView):
    # permission_classes -> for logged in users

    def get(self, request: Request, foreman_id: int):
        foreman = request.user.id if not foreman_id else foreman_id
        tasks = Tasks.objects.filter(Q(foreman=foreman))
        paginated_tasks = paginator.paginate_queryset(tasks, request)
        return paginator.get_paginated_response(TasksSerializer(paginated_tasks, many=True).data)


# tasks that are picked
class PickedTasks(APIView):
    # permission_classes -> for logged in users

    def get(self, request: Request):
        tasks = Tasks.objects.filter(Q(status=Tasks.Status.PICKED))
        paginated_tasks = paginator.paginate_queryset(tasks, request)
        return paginator.get_paginated_response(TasksSerializer(paginated_tasks, many=True).data)


# tasks that are done
class DoneTasks(APIView):
    # permission_classes -> for logged in users

    def get(self, request: Request):
        done_tasks_id_list = Tags.objects.filter(Q(
            title=Tags.Titles.DONE
        )).values_list('id', flat=True)

        tasks = Tasks.objects.filter(Q(
            id__in=done_tasks_id_list
        ))

        paginated_tasks = paginator.paginate_queryset(tasks, request)
        return paginator.get_paginated_response(TasksSerializer(paginated_tasks, many=True).data)


# project for manager logged in
class ProjectsManger(APIView):
    #  permission_classes -> loggin manager

    def get(self, request: Request):
        manager = request.query_params.get('manager-id') or request.user.id
        projects = Projects.objects.filter(
            Q(user=manager)
        )
        paginated_projects = paginator.paginate_queryset(projects, request)
        return paginator.get_paginated_response(ProjectSerializer(
            paginated_projects, many=True
        ).data)


# projects that are done
class DoneProjects(APIView):
    # permission_classes -> just for manager

    def get(self, request: Request):
        projects = Projects.objects.filter(
            Q(status=Projects.Status.DONE)
        )
        paginated_projects = paginator.paginate_queryset(projects, request)
        return paginator.get_paginated_response(ProjectSerializer(
            paginated_projects, many=True
        ).data)


# projects that are not done
class NotDoneProjects(APIView):
    # permission_classes -> just for manager

    def get(self, request: Request):
        projects = Projects.objects.filter(
            ~Q(status=Projects.Status.DONE)
        )
        paginated_projects = paginator.paginate_queryset(projects, request)
        return paginator.get_paginated_response(ProjectSerializer(
            paginated_projects, many=True
        ).data)


# the tasks are on a specific deadline date or after
class DeadLineTasks(APIView):
    # permission_classes -> the logged in

    def get(self, request: Request, dead_line):
        tasks = Tasks.objects.filter(
            Q(deadline__gte=dead_line)
        )
        paginated_tasks = paginator.paginate_queryset(
            tasks, request
        )
        return paginator.get_paginated_response(TasksSerializer(
            paginated_tasks, many=True
        ).data)


# the projects that are on specific deadline date
class DeadLineProjects(APIView):
    # permission_classes -> the logged in users
    def get(self, request: Request, deadline):
        projects = Projects.objects.filter(
            Q(deadline__gte=deadline)
        )
        paginated_projects = paginator.paginate_queryset(
            projects, request
        )
        return paginator.get_paginated_response(
            ProjectSerializer(
                paginated_projects, many=True
            ).data
        )


# projects that are a specific foreman in member in
class ProjectsForeman(APIView):
    # permission_classes -> logged in users
    def get(self, request: Request, foreman_id: int):
        foreman = request.user.id or foreman_id

        projects_id_list = ProjectMembers.objects.filter(
            Q(member=foreman)
        ).values_list('project', flat=True)

        projects = Projects.objects.filter(
            Q(id__in=projects_id_list)
        )

        paginated_projects = paginator.paginate_queryset(
            projects, request
        )

        return paginator.get_paginated_response(
            ProjectSerializer(
                paginated_projects, many=True
            ).data
        )
