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


# tags api
class TagsAPI(
    GenericViewSet, CreateModelMixin,
    ListModelMixin, RetrieveModelMixin
):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()


# scores api
class ScoresAPI(
    GenericViewSet, CreateModelMixin,
    ListModelMixin, RetrieveModelMixin
):
    serializer_class = ScoresSerializer
    queryset = Scores.objects.all()


# Memeber api
class MembersAPI(
    GenericViewSet, CreateModelMixin,
    ListModelMixin, RetrieveModelMixin
):
    serializer_class = ProjectMembersSerializer
    queryset = ProjectMembers.objects.all()
