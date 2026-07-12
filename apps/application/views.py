from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db import models
from apps.user.models import Master
from apps.user.permissions import IsMaster
from apps.notification.models import Notification
from .models import Application
from .serializers import ApplicationSerializer, ApplicationClientUpdateSerializer, ApplicationMasterUpdateSerializer
from .permissions import IsOwnerOrAssignedMasterOrAdmin


class ApplicationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        if u.is_superuser:
            return Application.objects.all()
        master = Master.objects.filter(user=u).first()
        if master:
            return Application.objects.filter(models.Q(user=u) | models.Q(master=master))
        return Application.objects.filter(user=u)


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
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAssignedMasterOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ("PATCH", "PUT"):
            u = self.request.user
            obj = self.get_object()
            if u.is_superuser:
                return ApplicationSerializer
            if obj.master_id and u == obj.master.user:
                return ApplicationMasterUpdateSerializer
            return ApplicationClientUpdateSerializer
        return ApplicationSerializer


class ApplicationAcceptAPIView(generics.GenericAPIView):
    queryset = Application.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        application = self.get_object()
        master = Master.objects.filter(user=request.user).first()

        if not master:
            return Response({"detail": "Siz usta emassiz"}, status=403)
        if application.status != "waiting":
            return Response({"detail": "Bu buyurtma allaqachon band"}, status=409)

        application.master = master
        application.status = "master_found"
        application.save(update_fields=["master", "status"])

        Notification.objects.create(
            title="Buyurtma qabul qilindi",
            content=f"{master.first_name} sizning buyurtmangizni qabul qildi",
            for_user=application.user,
        )
        return Response(ApplicationSerializer(application).data)