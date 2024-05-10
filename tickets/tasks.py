from celery import shared_task
from cloudinary.uploader import upload
from django.core.files.base import ContentFile
from .models import Ticket, Image


@shared_task
def handle_image_upload(image_data, file_name, ticket_id):
    # Convert image data to a ContentFile which is more suitable for upload processes
    image_file = ContentFile(image_data, name=file_name)

    # Upload the file to Cloudinary
    upload_result = upload(
        image_file, fetch_format="auto", quality="auto", resource_type="image"
    )
    image_url = upload_result["secure_url"]
    public_id = upload_result["public_id"]

    # Create and save the image instance
    ticket = Ticket.objects.get(id=ticket_id)
    Image.objects.create(ticket=ticket, image_url=image_url, public_id=public_id)

    # Update the ticket's current image count and check completion
    ticket.current_images += 1
    if ticket.current_images == ticket.total_images:
        ticket.status = "completed"
    ticket.save()
