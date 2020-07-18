from rest_framework import viewsets
from . import models
from . import serializers

class AllInterestsViewSet(viewsets.ModelViewSet):
    queryset = models.AllInterests.objects.all()
    serializer_class = serializers.AllInterestsSerializer
