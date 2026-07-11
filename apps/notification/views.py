from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
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