from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import UserProfile

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(write_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

# Login Serializer
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('email','mobile','password')
        extra_kwargs = {'password': {'write_only': True}}

# ViewProfile Serializer
class ViewProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('uname')
        