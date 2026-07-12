from rest_framework import permissions
from apps.user.models import Master

class IsAdminOrMine(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        master = Master.objects.filter(user=request.user).first()
        if not master:
            return False

        return obj.master == master or request.user.is_superuser


class IsSubscriptionOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        u = request.user
        return u.is_authenticated and (u.is_superuser or u == obj.master.user)