from rest_framework import serializers

from .models import Image
from .models import Ticket


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image_url", "public_id", "ticket", "uploaded_at"]


class TicketSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "status",
            "total_images",
            "current_images",
            "images",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "status",
            "current_images",
            "images",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        return Ticket.objects.create(
            user=user, status="pending", current_images=0, **validated_data
        )
