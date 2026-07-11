from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.user.models import Master
from apps.user.permissions import IsMaster
from apps.notification.models import Notification
from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsAdminOrMine


class ApplicationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        masters = Master.objects.filter(is_active=True, is_online=True, category=serializer.instance.category)
        for master in masters:
            Notification.objects.create(
                title="New Application",
                content=f"New Application. Type quickly",
                for_user=master.user
            )
        return Response(serializer.data, status=201)

class ApplicationDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminOrMine, IsMaster]