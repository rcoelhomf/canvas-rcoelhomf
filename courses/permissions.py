from rest_framework import permissions
from rest_framework.views import View
from courses.models import Course


class HaveUserPermission(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        if request.user.is_authenticated and request.user.is_superuser:
            return True

        course = Course.objects.get(pk=view.kwargs['course_id'])
        if (request.method in permissions.SAFE_METHODS) and len(course.students.filter(id=request.user.id)) >= 1:
            return True

        return False


class HavePermission(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_superuser


class IsAccountOwner(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        if request.user.is_authenticated and request.user.is_superuser:
            return True

        return False
