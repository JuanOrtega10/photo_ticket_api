from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Ticket, Image
from .serializers import TicketSerializer, ImageSerializer
from .tasks import upload_image_to_cloudinary


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
        file = request.FILES.get('file')  # Get the file from the request
        if not file:
            return Response({'error': 'No file provided.'}, status=400)

        # Save the file temporarily and send it to Celery task
        temp_file_path = file.temporary_file_path()
        upload_image_to_cloudinary.delay(temp_file_path, ticket_id)

        return Response({'status': 'Upload in progress'}, status=202)

class TicketDetailViewSet(viewsets.GenericViewSet):
    queryset = Ticket.objects.none()
    serializer_class = TicketSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)