from rest_framework import serializers

from .models import Image
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'user', 'created_at', 'updated_at', 'status', 'total_images']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'status']

    def create(self, validated_data):
        user = self.context['request'].user
        return Ticket.objects.create(user=user, status='pending', **validated_data)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
