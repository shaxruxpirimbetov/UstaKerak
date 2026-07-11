from rest_framework import permissions


class IsAdminOrMe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj or request.user.is_superuser


class IsAdminOrMine(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user or request.user.is_superuser