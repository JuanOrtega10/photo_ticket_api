from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, TicketImageViewSet, TicketDetailViewSet
from django.urls import include, path

router = DefaultRouter()
router.register(r"tickets", TicketViewSet, basename="tickets")

urlpatterns = [
    path("", include(router.urls)),
    # Specific route for uploading images to a ticket
    path("tickets/<int:ticket_id>/images/", TicketImageViewSet.as_view({
        "post": "create"
    }), name="ticket-images"),
    # Specific route for viewing details of a ticket
    path("tickets/<int:ticket_id>/", TicketDetailViewSet.as_view({
        "get": "retrieve"
    }), name="ticket-detail"),
]