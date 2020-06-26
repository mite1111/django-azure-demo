from ticketapi.viewsets import TicketDetailsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('ticketapi',TicketDetailsViewSet)