from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsersAPI, ProjectsAPI, TasksAPI, TasksManager,
    TasksProject, TasksForeman, PickedTasks, DoneTasks, ProjectsManger,
    DoneProjects, NotDoneProjects, DeadLineTasks
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
    ),
    path(
        'tasks-project/<int:project_id>/', TasksProject.as_view(), name='tasks-project'
    ),
    path(
        'tasks-foreman/<int:foreman_id>/', TasksForeman.as_view(), name='tasks-foreman',
    ),
    path(
        'picked-tasks/', PickedTasks.as_view(), name='picked-tasks',
    ),
    path(
        'done-tasks/', DoneTasks.as_view(), name='done-tasks/',
    ),
    path(
        'projects-manager/', ProjectsManger.as_view(), name='projects-manager',
    ),
    path(
        'done-projects/', DoneProjects.as_view(), name='done-projects',
    ),
    path(
        'not-done-projects/', NotDoneProjects.as_view(), name='not-done-projects'
    ),
    path(
        'deadline-tasks/<dead_line>/', DeadLineTasks.as_view(), name='DeadLineTasks'
    )
]
