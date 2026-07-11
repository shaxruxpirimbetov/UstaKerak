from rest_framework import generics, permissions
from apps.user.permissions import IsMaster
from .models import Subscription
from .serializers import SubscriptionSerializer
from .permissions import IsAdminOrMine

class SubscriptionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class SubscriptionDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [IsAdminOrMine()]