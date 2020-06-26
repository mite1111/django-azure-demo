from rest_framework import viewsets
from . import models
from . import serializers

class TicketDetailsViewSet(viewsets.ModelViewSet):
    queryset = models.ticketDetails.objects.all()
    serializer_class = serializers.ticketDetailsSerializer