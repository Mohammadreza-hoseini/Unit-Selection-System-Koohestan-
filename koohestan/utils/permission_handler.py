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


class StudentSelfPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 1 and request.user.id == str(view.kwargs['pk']):
            return request.user and request.user.is_authenticated


class EASelfPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 4 and request.user.id == str(view.kwargs['pk']):
            return request.user and request.user.is_authenticated


class ProfessorSelfPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 2 and request.user.id == str(view.kwargs['pk']):
            return request.user and request.user.is_authenticated

class ProfessorSelf_ITPermission(BasePermission):
    def has_permission(self, request, view):
        if (request.user.role == 2 and request.user.professor_user_role.id == str(view.kwargs['pk'])) or (request.user.role == 3):
            return request.user and request.user.is_authenticated