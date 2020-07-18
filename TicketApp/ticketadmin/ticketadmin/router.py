from ticketapi.viewsets import TicketDetailsViewSet
from interestsapi.viewsets import AllInterestsViewSet
from commentsapi.viewsets import CommentsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('ticketapi',TicketDetailsViewSet)
router.register('interestsapi',AllInterestsViewSet)
router.register('commentsapi',CommentsViewSet)
