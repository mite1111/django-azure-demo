from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ViewProfileSerializer
from django.db import connection
from django.http import HttpResponse
import random
import json
import uuid
from datetime import datetime
from django.http import JsonResponse

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    #def post(self, request, *args, **kwargs):
        #serializer = self.get_serializer(data=request.data)
        #serializer.is_valid(raise_exception=True)
        #user = serializer.save()
        #return Response({
        #"user": UserSerializer(user, context=self.get_serializer_context()).data
        # "token": AuthToken.objects.create(user)[1]
        #})

    def post(self, request):
        if request.method == "POST":
            name = request.data['name']
            email = request.data['email']
            password = request.data['password']
            preference = request.data['preference']
            profile_type = request.data['profile_type']
            mobile = request.data['mobile']
            city = request.data['city']
            state = request.data['state']
            country = request.data['country']
            subscription_type = request.data['subscription_type']
            datecreated = str(datetime.utcnow())
            dateupdated = str(datetime.utcnow())
            auth_key = ''
            
            cursor = connection.cursor()
            cursor.execute("INSERT INTO user_profile(name,email,password,preference,profile_type,mobile,city,state,country,subscription_type,datecreated,dateupdated,auth_key) values(%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s) RETURNING user_id",[name, email, password, preference, profile_type, mobile, city, state, country, subscription_type, datecreated, dateupdated, auth_key])
            
            if cursor.rowcount >= 1:
                rows = cursor.fetchall()
                for row in rows:
                    user_id = row[0]
                data = {
                        'user_id': user_id
                        }
                return Response(data)
            else:
                return Response({"response":"Error saving user info"})

# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        if request.method == "POST":
            if request.data['email'] and request.data['password']:
                email = request.data['email']
                password = request.data['password']

                cursor = connection.cursor()
                cursor.execute("SELECT user_id, name, city, email, mobile FROM user_profile WHERE email = %s AND password = %s",[email, password])
                
                if cursor.rowcount >= 1:
                    rows = cursor.fetchall()
                    for row in rows:
                        user_id = row[0]
                        name = row[1]
                        city = row[2]
                        email = row[3]
                        mobile = row[4]
                    auth_key = uuid.uuid1()
                    cursor.execute("UPDATE user_profile SET auth_key = %s WHERE user_id = %s",[auth_key, user_id])
                    data = {
                            'user_id': user_id,
                            'name': name,
                            'city': city,
                            'email': email,
                            'mobile': mobile,
                            'auth_key': auth_key
                            }
                    return Response(data)
                else:
                    return Response({"response":"Incorrect Credentials"})
            else:
                return Response({"response":"Please send email and password to login"})

# ViewProfile API
class ViewProfileAPI(APIView):
    serializer_class = ViewProfileSerializer
    
    def get(self, request):
        if request.GET.get('user_id') and request.GET.get('name') and request.GET.get('auth_key'):
            user_id = request.GET.get('user_id')
            name = request.GET.get('name')
            auth_key = request.GET.get('auth_key')

            cursor = connection.cursor()
            cursor.execute("SELECT name,email,preference,profile_type,mobile,city,state,country,subscription_type FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])

            if cursor.rowcount >= 1:
                rows = cursor.fetchall()
                for row in rows:
                    name = row[0]
                    email = row[1]
                    preference = row[2]
                    profile_type = row[3]
                    mobile = row[4]
                    city = row[5]
                    state = row[6]
                    country = row[7]
                    subscription_type = row[8]
                data = {
                            'name': name,
                            'email': email,
                            'preference': preference,
                            'profile_type': profile_type,
                            'mobile': mobile,
                            'city': city,
                            'state': state,
                            'country': country,
                            'subscription_type': subscription_type,
                        }
                return Response(data)
            else:
                return Response({"response":"User does not exist OR Incorrect query params"})
        else:
                return Response({"response":"Incorrect number of Query parameters"})


# EditProfile API
class EditProfile(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        if request.method == "POST":
            user_id = request.data['user_id']
            auth_key = request.data['auth_key']
            name = request.data['name']
            email = request.data['email']
            preference = request.data['preference']
            profile_type = request.data['profile_type']
            mobile = request.data['mobile']
            city = request.data['city']
            state = request.data['state']
            country = request.data['country']
            subscription_type = request.data['subscription_type']
            dateupdated = str(datetime.utcnow())
            
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])
            #cursor.execute("INSERT INTO user_profile(name,email,password,preference,profile_type,mobile,city,state,country,subscription_type,datecreated,dateupdated,auth_key) values(%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s) RETURNING user_id",[name, email, password, preference, profile_type, mobile, city, state, country, subscription_type, datecreated, dateupdated, auth_key])
            
            if cursor.rowcount >= 1:
                cursor.execute("UPDATE user_profile SET name = %s, email = %s, preference = %s, profile_type = %s, mobile = %s, city = %s, state = %s, country = %s, subscription_type = %s, dateupdated = %s WHERE user_id = %s RETURNING user_id",[name, email, preference, profile_type, mobile, city, state, country, subscription_type, dateupdated, user_id])
                rows = cursor.fetchall()
                for row in rows:
                    user_id = row[0]
                data = {
                        'user_id': user_id
                        }
                return Response(data)
            else:
                return Response({"response":"Error while updating user info"})
