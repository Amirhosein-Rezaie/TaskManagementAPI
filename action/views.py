from rest_framework.viewsets import (
    ModelViewSet, GenericViewSet
)
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin,
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
)
from .models import (
    Tags, ProjectMembers, Scores
)
from .serializers import (
    TagsSerializer, ScoresSerializer, ProjectMembersSerializer
)
from rest_framework.request import Request
from TaskManagementAPI.helper import (
    dynamic_search, limit_paginate
)
from TaskManagementAPI.pagination import (
    DynamicPagination
)
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework.response import Response
from core.models import (
    Users
)


# tags api
class TagsAPI(
    GenericViewSet, CreateModelMixin,
    ListModelMixin, RetrieveModelMixin
):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    pagination_class = DynamicPagination

    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(
                request=request, model=Tags, serializer=TagsSerializer,
                pagination_class=DynamicPagination()
            )
        return super().list(request, *args, **kwargs)


# scores api
class ScoresAPI(
    GenericViewSet, CreateModelMixin,
    ListModelMixin, RetrieveModelMixin
):
    serializer_class = ScoresSerializer
    queryset = Scores.objects.all()
    pagination_class = DynamicPagination

    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(
                request=request, model=Scores, serializer=ScoresSerializer,
                pagination_class=DynamicPagination()
            )
        return super().list(request, *args, **kwargs)


# Memeber api
class MembersAPI(
    GenericViewSet, CreateModelMixin,
    ListModelMixin, RetrieveModelMixin
):
    serializer_class = ProjectMembersSerializer
    queryset = ProjectMembers.objects.all()
    pagination_class = DynamicPagination

    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(
                request=request, model=ProjectMembers, serializer=ProjectMembersSerializer,
                pagination_class=DynamicPagination()
            )
        return super().list(request, *args, **kwargs)


# paginator
paginator = DynamicPagination()


# the tags are for a specific foreman
class ForemanTags(APIView):
    # permission_classes -> for logged in user

    def get(self, request: Request):
        foreman = request.query_params.get('foreman') or request.user.id
        if not foreman:
            raise ValidationError(
                detail="No parameter found as foreman ID"
            )
        try:
            if Users.objects.get(Q(id=foreman)).role != Users.Roles.FOREMAN:
                raise ValidationError(
                    detail="This user is not foreman"
                )
        except Users.DoesNotExist as e:
            raise ValidationError(
                detail="User not found"
            )
        tags = Tags.objects.filter(
            Q(user=foreman)
        )
        paginator.page_size = limit_paginate(request, DynamicPagination)
        paginated_data = paginator.paginate_queryset(
            tags, request
        )
        return paginator.get_paginated_response(
            TagsSerializer(paginated_data, many=True).data
        )
