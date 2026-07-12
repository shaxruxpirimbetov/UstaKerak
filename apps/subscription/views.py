from rest_framework import generics, permissions
from apps.user.permissions import IsMaster
from .models import Subscription
from .serializers import SubscriptionSerializer
from .permissions import IsAdminOrMine, IsSubscriptionOwnerOrAdmin

class SubscriptionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        if u.is_superuser:
            return Subscription.objects.all()
        return Subscription.objects.filter(master__user=u)

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class SubscriptionDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsSubscriptionOwnerOrAdmin]