from rest_framework import serializers
from .models import ticketDetails
from rest_framework.decorators import api_view
from django.conf import settings

# @api_view(['POST'])


class ticketDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ticketDetails
        fields = '__all__'    

    # def validate_Auth_Key(self, value):
    #     if 'woohoo' not in value.lower():
    #         raise serializers.ValidationError("Incorrect Auth_key")
    #     return value

    def validate_Auth_Key(self, value):
        if value != settings.AUTH_KEY:
            raise serializers.ValidationError("Incorrect Auth_key")
        return value
    # def create(self, validated_data):
    #     meals = validated_data.pop('meals')
    #     instance = Order.objects.create(**validated_data)
    #     for meal in meals:
    #         instance.meals.add(meal)

    #     return instance

        