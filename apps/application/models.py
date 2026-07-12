from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from apps.category.models import Category
from apps.user.models import Master

User = get_user_model()

application_status_choices = [
    ("waiting", "Qidirilmoqda"),        # заявка создана, идёт подбор мастера
    ("master_found", "Usta topildi"),   # мастер назначен, ждём его подтверждения/выезда
    ("on_the_way", "Yo'lda"),           # мастер выехал
    ("in_progress", "Ishlanmoqda"),     # мастер работает на месте
    ("completed", "Yakunlandi"),        # успешно завершено
    ("cancelled", "Bekor qilindi"),     # отменено клиентом/мастером/системой
]

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='application_user')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='application_category')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='application_master', null=True, blank=True)
    problem = models.TextField(validators=[MinLengthValidator(10), MaxLengthValidator(1000)])
    address = models.CharField(max_length=124)
    address_latlng = models.JSONField()
    is_asap = models.BooleanField(default=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=24, choices=application_status_choices, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering = ['-created_at']