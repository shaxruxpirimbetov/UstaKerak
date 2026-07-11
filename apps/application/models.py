from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from apps.user.models import Master

User = get_user_model()

application_status_choices = [
    ("waiting", "Waiting"),
    ("processing", "Processing"),
    ("ended", "Ended"),
]

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='application_user')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='application_master', null=True, blank=True)
    problem = models.TextField(validators=[MinLengthValidator(10), MaxLengthValidator(1000)])
    address = models.CharField(max_length=124)
    address_latlng = models.JSONField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=application_status_choices, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering = ['-created_at']