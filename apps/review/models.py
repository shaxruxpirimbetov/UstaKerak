from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
from apps.application.models import Application
from apps.user.models import Master

User = get_user_model()


class Review(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="review_application")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_user")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name="review_master")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(validators=[MinLengthValidator(5), MaxLengthValidator(500)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application} - {self.user} - {self.master} | {self.rating}"

    class Meta:
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']