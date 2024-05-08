from rest_framework import viewsets, permissions
from .models import Ticket, Image
from .serializers import TicketSerializer, ImageSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.none()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.none()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(ticket__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(ticket=Ticket.objects.filter(user=self.request.user, id=self.request.data.get('ticket')).first())
