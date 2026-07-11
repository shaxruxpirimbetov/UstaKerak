from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    for_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='for_user')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']