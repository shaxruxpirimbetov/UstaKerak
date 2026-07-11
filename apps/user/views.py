from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, parsers
from rest_framework.response import Response

from .models import Master, MasterPortfolioPhotos
from .serializers import UserSerializer, MasterSerializer, MasterOnlineSerializer
from .permissions import IsAdminOrMe, IsAdminOrMine

User = get_user_model()

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrMe]


class MasterListCreateAPIView(generics.ListCreateAPIView):
    parser_classes = [parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser]
    queryset = Master.objects.all()
    serializer_class = MasterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        images = request.FILES.getlist("master_portfolio_photos")

        for image in images:
            MasterPortfolioPhotos.objects.create(master=serializer.instance, photo=image)
        return Response(serializer.data, status=201)


class MasterDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [IsAdminOrMine()]


class MasterOnlineToggleAPIView(generics.UpdateAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterOnlineSerializer  # только поле is_online
    permission_classes = [IsAdminOrMine]