from rest_framework import serializers
from .models import ticketDetails

class ticketDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ticketDetails
        fields = '__all__'