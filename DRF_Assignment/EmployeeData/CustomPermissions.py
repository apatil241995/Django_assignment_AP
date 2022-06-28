from rest_framework.permissions import BasePermission


class IsManager(BasePermission):

    def has_permission(self, request, view):
        pass


class IsEmployee(BasePermission):
    massage = 'Employee has no permission to create employee entries'

    def has_object_permission(self, request, view, obj):
        pass