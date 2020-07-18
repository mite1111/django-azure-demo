from rest_framework import serializers
from .models import AllInterests
from django.conf import settings

class AllInterestsSerializer(serializers.ModelSerializer):

    auth_key = serializers.CharField(write_only=True)

    class Meta:
        model = AllInterests
        fields = '__all__' 
