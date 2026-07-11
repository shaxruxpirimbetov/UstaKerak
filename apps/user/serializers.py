from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Master

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = "__all__"