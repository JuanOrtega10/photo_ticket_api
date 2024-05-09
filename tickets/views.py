from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Ticket, Image
from .serializers import TicketSerializer, ImageSerializer
from .tasks import handle_image_upload


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.none()
    serializer_class = TicketSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Ticket.objects.filter(user=self.request.user)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        status = self.request.query_params.get('status')

        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        if status:
            queryset = queryset.filter(status=status)

        return queryset
class TicketImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.none()
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser]  # To handle file uploads in the request
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = get_object_or_404(Ticket, pk=ticket_id)

        # Check if the ticket has reached its limit of images
        if ticket.current_images == ticket.total_images or ticket.status == 'completed':
            return Response({'error': 'All images for this ticket have already been uploaded. The ticket is complete.'},
                            status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Enqueue the image for processing and upload
        handle_image_upload.delay(file.read(), file.name, ticket_id)

        return Response({'status': 'Upload in progress'}, status=status.HTTP_202_ACCEPTED)

class TicketDetailViewSet(viewsets.GenericViewSet):
    queryset = Ticket.objects.none()
    serializer_class = TicketSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Ticket.objects.prefetch_related('images'), pk=kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)