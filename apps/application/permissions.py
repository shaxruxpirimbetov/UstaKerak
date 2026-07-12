from rest_framework import permissions
from apps.user.models import Master


class IsAdminOrMine(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (request.user == obj.user or request.user == obj.master.user) or request.user.is_superuser


class IsOwnerOrAssignedMasterOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        u = request.user
        if not u.is_authenticated:
            return False
        return u.is_superuser or u == obj.user or (obj.master_id and u == obj.master.user)