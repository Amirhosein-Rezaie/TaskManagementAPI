from django.urls import path, include
from .views import (
    TagsAPI, ScoresAPI, MembersAPI,
)
from rest_framework.routers import DefaultRouter

# routers
# tags
tags_router = DefaultRouter()
tags_router.register('', TagsAPI)

# scores
scores_router = DefaultRouter()
scores_router.register('', ScoresAPI)

# project members
members_router = DefaultRouter()
members_router.register('', MembersAPI)

# urls
urlpatterns = [
    path(
        'tags/', include(tags_router.urls), name='tags'
    ),
    path(
        'scores/', include(scores_router.urls), name='scores'
    ),
    path(
        'project-members/', include(members_router.urls), name='project-membres'
    )
]
