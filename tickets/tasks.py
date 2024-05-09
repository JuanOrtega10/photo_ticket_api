from celery import shared_task
from cloudinary.uploader import upload
from .models import Ticket, Image


@shared_task
def upload_image_to_cloudinary(image_path, ticket_id):
    upload_result = upload(image_path)
    image_url = upload_result["secure_url"]
    public_id = upload_result["public_id"]

    # Create and save the image instance
    ticket = Ticket.objects.get(id=ticket_id)
    Image.objects.create(ticket=ticket, image_url=image_url, public_id=public_id)

    # Update the ticket's current image count
    ticket.current_images += 1
    if ticket.current_images >= ticket.total_images:
        ticket.status = 'completed'
    ticket.save()
