from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .models import Master
from .serializers import UserSerializer, MasterSerializer
from .permissions import IsAdminOrMe, IsAdminOrMine

User = get_user_model()

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrMe]


class MasterListCreateAPIView(generics.ListCreateAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MasterDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [IsAdminOrMine()]