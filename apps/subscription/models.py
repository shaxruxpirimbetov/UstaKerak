from django.db import models
from apps.user.models import Master

class Subscription(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name="subscriptions")
    status = models.CharField(choices=[("active","Active"),("expired","Expired"),("pending","Pending")], default="pending")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
