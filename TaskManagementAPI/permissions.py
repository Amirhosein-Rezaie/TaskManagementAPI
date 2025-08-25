from rest_framework.permissions import (
    BasePermission
)
from rest_framework.request import Request
from core.models import (
    Users
)


# is manager
class IsManagerUser(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(
            (request.user or request.user.is_authenticated) and
            (request.user.role == Users.Roles.MANAGER)
        )


# is Foreman
class IsForemanUser(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(
            (request.user or request.user.is_authenticated) and
            (request.user.role == Users.Roles.FOREMAN)
        )
