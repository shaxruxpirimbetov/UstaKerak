from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsAdminOrMine


class NotificationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Notification.objects.all()
        return Notification.objects.filter(for_user=self.request.user)

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)

        if request.user.is_authenticated:
            for notification in serializer.instance:
                if notification.for_user == request.user:
                    notification.is_read = True
                    notification.save(update_fields=["is_read"])

        return Response(serializer.data)


class NotificationDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]