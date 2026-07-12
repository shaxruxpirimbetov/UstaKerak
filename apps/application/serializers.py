from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

    def validate(self, data):
        if not data.get("is_asap", True) and not data.get("scheduled_at"):
            raise serializers.ValidationError("Agar 'hozir' bo'lmasa, vaqtni tanlang")
        return data

class ApplicationClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status"]  # клиенту доступна только отмена

    def validate_status(self, value):
        if value != "cancelled":
            raise serializers.ValidationError("Mijoz faqat bekor qila oladi")
        return value

class ApplicationMasterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status"]

    def validate_status(self, value):
        allowed = ["on_the_way", "in_progress", "completed"]
        if value not in allowed:
            raise serializers.ValidationError("Usta bu statusni qo'ya olmaydi")
        return value