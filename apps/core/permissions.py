
from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()


class RoleBasePermission(BasePermission):
    required_role = None

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        required_rank = User.ROLE_HIERARCHY.get(
            self.required_role
        )

        if required_rank is None:
            return False

        return user.role_rank >= required_rank


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.CLIENT
        )


class IsOfficerOrAbove(RoleBasePermission):
    required_role = User.Role.OFFICER


class IsSeniorOfficer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.SENIOR_OFFICER
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_authenticated
            and user.role == User.Role.ADMIN
        )
