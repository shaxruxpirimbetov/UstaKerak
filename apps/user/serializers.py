from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Master, MasterPortfolioPhotos

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "phone", "region", "password"]  # НЕ "__all__"
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class MasterPortfolioPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterPortfolioPhotos
        fields = "__all__"

class MasterSerializer(serializers.ModelSerializer):
    master_portfolio_photos = MasterPortfolioPhotosSerializer(read_only=True, many=True)
    class Meta:
        model = Master
        fields = "__all__"


class MasterOnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ["is_online"]