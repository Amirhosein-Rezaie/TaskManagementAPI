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
from drf_spectacular.utils import (
    OpenApiExample, OpenApiParameter, OpenApiResponse, extend_schema
)


# views
# users view
class UsersAPI(ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users.objects.all()

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
@extend_schema(
    description="a API for manager that logged in",
    responses=TasksSerializer(many=True)
)
class TasksManager(APIView):
    # permission_classes -> allow for logged in managers

    def get(self, request: Request):
        manager = request.user
        tasks = Tasks.objects.filter(
            Q(user=manager.id)
        )
        paginated_tasks = paginator.paginate_queryset(
            tasks, request
        )
        return paginator.get_paginated_response(
            TasksSerializer(
                paginated_tasks, many=True
            ).data
        )


# tasks that is for specific project
@extend_schema(
    description="An API of tasks for a specific project.",
    responses=TasksSerializer(many=True),
)
class TasksProject(APIView):
    # permission_classes -> for logged in users

    def get(self, request: Request, project_id: int):
        tasks = Tasks.objects.filter(
            Q(project=project_id)
        )
        paginated_tasks = paginator.paginate_queryset(
            tasks, request
        )
        return paginator.get_paginated_response(
            TasksSerializer(
                paginated_tasks, many=True
            ).data
        )


# tasks that is picked by a specific foreman
@extend_schema(
    description="An API of tasks for a specific foreman (logged in or by foreman_id)",
    parameters=[
        OpenApiParameter(
            name="foreman_id", type=int, location=OpenApiParameter.PATH, required=False,
            description="Optional foreman ID. If not provided, current logged in user is used."
        )
    ],
    responses=TasksSerializer(many=True)
)
class TasksForeman(APIView):
    # permission_classes -> for logged in users

    def get(self, request: Request, foreman_id: int):
        foreman = request.user.id if not foreman_id else foreman_id
        tasks = Tasks.objects.filter(
            Q(foreman=foreman)
        )
        paginated_tasks = paginator.paginate_queryset(
            tasks, request
        )
        return paginator.get_paginated_response(
            TasksSerializer(
                paginated_tasks, many=True
            ).data
        )


# tasks that are picked
@extend_schema(
    description="An API of tasks that are pick by one of foremans.",
    responses=TasksSerializer(many=True)
)
class PickedTasks(APIView):
    # permission_classes -> for logged in users

    def get(self, request: Request):
        tasks = Tasks.objects.filter(
            Q(status=Tasks.Status.PICKED)
        )
        paginated_tasks = paginator.paginate_queryset(
            tasks, request
        )
        return paginator.get_paginated_response(
            TasksSerializer(
                paginated_tasks, many=True
            ).data
        )


# tasks that are done
@extend_schema(
    description="An API of tasks that are done by one of foremans.",
    responses=TasksSerializer(many=True)
)
class DoneTasks(APIView):
    # permission_classes -> for logged in users

    def get(self, request: Request):
        done_tasks_id_list = Tags.objects.filter(Q(
            title=Tags.Titles.DONE
        )).values_list('id', flat=True)

        tasks = Tasks.objects.filter(Q(
            id__in=done_tasks_id_list
        ))

        paginated_tasks = paginator.paginate_queryset(
            tasks, request
        )
        return paginator.get_paginated_response(
            TasksSerializer(
                paginated_tasks, many=True
            ).data
        )


# project for manager logged in
@extend_schema(
    description="An API of projcets that are added by specific manager.",
    parameters=[
        OpenApiParameter(
            name='manager-id', type=int, required=False,
            description="If manager is logged in this parameter is not required."
        )
    ],
    responses=ProjectSerializer(many=True),
)
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
@extend_schema(
    description="An API of projcets that are done",
    responses=ProjectSerializer(many=True),
)
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
@extend_schema(
    description="An API of projcets that are not done yet",
    responses=ProjectSerializer(many=True),
)
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
@extend_schema(
    description="An API of tasks that are on a specific deadline date.",
    responses=TasksSerializer(many=True)
)
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
@extend_schema(
    description="An API of projcets that are on a specific deadline date.",
    responses=ProjectSerializer(many=True),
)
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
@extend_schema(
    description="An API of projcets that a specific foreman had been member in it.",
    parameters=[
        OpenApiParameter(
            name='foreman_id', type=int, required=False,
            description="If foreman logged in , it is not required to send this parameter.",
        )
    ],
    responses=ProjectSerializer(many=True),
)
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


# collaborators (foremans) of a specific project
@extend_schema(
    description="An API for foremans that are in a specific project",
    responses=UsersSerializer(many=True)
)
class MembersProject(APIView):
    # permission_classes -> manager
    def get(self, request: Request, project_id: int):
        project = project_id
        members = Users.objects.filter(
            Q(id__in=ProjectMembers.objects.filter(
                Q(project=project)
            ).values_list('member', flat=True))
        )
        paginated_data = paginator.paginate_queryset(
            members, request
        )
        return paginator.get_paginated_response(
            UsersSerializer(paginated_data, many=True).data
        )
