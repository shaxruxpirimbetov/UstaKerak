from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator
from django.db import models
from apps.category.models import Category


class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True)
    region = models.CharField(max_length=100, default='Nukus')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Master(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='master_user', unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    avatar = models.ImageField(upload_to='avatars/')
    bio = models.TextField(validators=[MinLengthValidator(5), MaxLengthValidator(1050)])
    experience_year = models.FloatField(validators=[MinValueValidator(0)], default=0)
    working_area = models.CharField(max_length=100, default='Nukus')
    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="master_category")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}, {self.first_name}, {self.last_name}, {self.category}"

    class Meta:
        verbose_name = 'Master'
        verbose_name_plural = 'Masters'
        ordering = ['-created_at']