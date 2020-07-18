from rest_framework import serializers
from .models import AllComments
from django.conf import settings

class AllCommentsSerializer(serializers.ModelSerializer):

    auth_key = serializers.CharField(write_only=True)

    class Meta:
        model = AllComments
        fields = '__all__'