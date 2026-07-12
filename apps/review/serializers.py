from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

    def validate_application(self, application):
        if application.status != "completed":
            raise serializers.ValidationError("Faqat yakunlangan buyurtmaga sharh qoldirish mumkin")
        if Review.objects.filter(application=application).exists():
            raise serializers.ValidationError("Bu buyurtmaga sharh allaqachon qoldirilgan")
        return application