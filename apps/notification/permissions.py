from rest_framework import permissions

class IsAdminOrMine(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.for_user == request.user or request.user.is_superuser