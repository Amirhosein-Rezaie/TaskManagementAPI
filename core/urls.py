from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsersAPI, ProjectsAPI, TasksAPI, TasksManager,
)

# routers
# user routers
users_router = DefaultRouter()
users_router.register('', UsersAPI)

# project routers
projects_router = DefaultRouter()
projects_router.register('', ProjectsAPI)

# tasks routers
tasks_router = DefaultRouter()
tasks_router.register('', TasksAPI, basename='all-tasks')

# urls
urlpatterns = [
    path(
        'users/', include(users_router.urls), name='all-users'
    ),
    path(
        'projects/', include(projects_router.urls), name='all-projects'
    ),
    path(
        'tasks/', include(tasks_router.urls), name='all-tasks'
    ),
    path(
        'tasks-manager/', TasksManager.as_view(), name='tasks-managet'
    )
]
