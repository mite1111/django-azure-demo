from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import TicketDetails

# PostTicket Serializer
class PostTicketSerializer(serializers.ModelSerializer):
    auth_key = serializers.CharField(write_only=True)
    
    class Meta:
        model = TicketDetails
        fields = '__all__'

# EditTicket Serializer
class EditTicketSerializer(serializers.ModelSerializer):
    auth_key = serializers.CharField(write_only=True)
    ticket_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = TicketDetails
        fields = '__all__'

