from rest_framework.permissions import BasePermission


class ITManagerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 3:
            return request.user and request.user.is_authenticated


class StudentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 1:
            return request.user and request.user.is_authenticated


class EducationalAssistantPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 4:
            return request.user and request.user.is_authenticated


class ProfessorPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 2:
            return request.user and request.user.is_authenticated
