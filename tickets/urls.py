from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, ImageViewSet
from django.urls import include, path

router = DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
