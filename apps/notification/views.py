from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsRecipientOrAdmin


class NotificationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
             notifications = Notification.objects.all()
        else:
            notifications = Notification.objects.filter(for_user=self.request.user)
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
    permission_classes = [permissions.IsAuthenticated, IsRecipientOrAdmin]