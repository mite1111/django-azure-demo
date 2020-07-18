from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import status
from rest_framework.response import Response

class TicketDetailsViewSet(viewsets.ModelViewSet):
    queryset = models.TicketDetails.objects.all()
    serializer_class = serializers.PostTicketSerializer
    