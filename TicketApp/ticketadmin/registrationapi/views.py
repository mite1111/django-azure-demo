from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ViewProfileSerializer, ChangePasswordSerializer
from django.db import connection
from django.http import HttpResponse
import random
import json
import uuid
from datetime import datetime, date
from django.http import JsonResponse
from django.db import IntegrityError
from dateutil import relativedelta
# from .models import UserProfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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
        try: 
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
                no_of_tickets_posted = 0
                
                is_image_upload = request.FILES['profile_picture'] if 'profile_picture' in request.FILES else False

                if is_image_upload == False:
                    path = ''
                else:
                    profile_picture = request.FILES['profile_picture']
                    actual_filename = request.FILES['profile_picture'].name
                    uploaded_filename = str(datetime.utcnow().strftime('%Y%m%d%H%M%S')) + "_" + actual_filename
                    uploaded_filepath = 'documents/profile_pictures/'+ str(datetime.utcnow().year) + '/' + str(datetime.utcnow().month) + '/' + str(datetime.utcnow().day) + '/' + uploaded_filename
                    path = default_storage.save(uploaded_filepath, ContentFile(profile_picture.read()))

                cursor = connection.cursor()
                cursor.execute("INSERT INTO user_profile(name,email,password,preference,profile_type,mobile,city,state,country,subscription_type,datecreated,dateupdated,auth_key,no_of_tickets_posted,profile_picture) values(%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s, %s, %s) RETURNING user_id",[name, email, password, preference, profile_type, mobile, city, state, country, subscription_type, datecreated, dateupdated, auth_key, no_of_tickets_posted,path])

                if cursor.rowcount >= 1:
                    rows = cursor.fetchall()
                    for row in rows:
                        user_id = row[0]
                    data = {
                            'user_id': user_id
                            }
                    cursor.close()
                    connection.close()

                    return Response(data)
                else:
                    return Response({"response":"Error saving user info"})
        
        except IntegrityError as e: 
            if 'unique constraint' in e.args[0]:
                return Response({"response":"Error saving user info. Mobile Number or Email already exists","stacktrace":e.args[0]})
        
        except Exception as e: 
            return Response({"response":"Error saving user info", "stacktrace":e.args[0]})

# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        try: 
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
                        
                        cursor.close()
                        connection.close()
                        
                        return Response(data)
                    else:
                        return Response({"response":"Incorrect Credentials"})
                else:
                    return Response({"response":"Please send email and password to login"})
        
        except Exception as e: 
            return Response({"response":"Error while Login", "stacktrace":e.args[0]})

# ViewProfile API
class ViewProfileAPI(APIView):
    serializer_class = ViewProfileSerializer
    
    def get(self, request):
        try:
            if request.GET.get('user_id') and request.GET.get('name') and request.GET.get('auth_key'):
                user_id = request.GET.get('user_id')
                name = request.GET.get('name')
                auth_key = request.GET.get('auth_key')

                cursor = connection.cursor()
                cursor.execute("SELECT name,email,preference,profile_type,mobile,city,state,country,subscription_type,no_of_tickets_posted,datecreated,profile_picture FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])

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
                        no_of_tickets_posted = row[9]
                        datecreated = str(row[10].strftime('%Y-%m-%d %H:%M:%S'))
                        
                        date1 = datetime.strptime(str(datecreated), '%Y-%m-%d %H:%M:%S')
                        current_date = datetime.strptime(str(str(datetime.utcnow().date())), '%Y-%m-%d')
                        r = relativedelta.relativedelta(current_date, date1)
                        member_since = str(r.years) + " Years " + str(r.months) + " Months " + str(r.days) + " Days"
                        profile_picture = row[11]

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
                                'no_of_tickets_posted': no_of_tickets_posted,
                                'datecreated': datecreated,
                                'member_since': member_since,
                                'profile_picture': profile_picture
                            }
                   
                    cursor.close()
                    connection.close()

                    return Response(data)
                else:
                    return Response({"response":"User does not exist OR Incorrect query params"})
            else:
                    return Response({"response":"Incorrect number of Query parameters"})
        
        except Exception as e: 
            return Response({"response":"Error while getting profile info", "stacktrace":e.args[0]})

# ViewOtherProfile API
class ViewOtherProfileAPI(APIView):
    serializer_class = ViewProfileSerializer
    
    def get(self, request):
        try:
            if request.GET.get('user_id') and request.GET.get('name') and request.GET.get('auth_key') and request.GET.get('other_user_id'):
                user_id = request.GET.get('user_id')
                name = request.GET.get('name')
                auth_key = request.GET.get('auth_key')
                other_user_id = request.GET.get('other_user_id')

                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])
                
                if cursor.rowcount >= 1:
                    cursor.execute("SELECT name,email,preference,profile_type,mobile,city,state,country,subscription_type,no_of_tickets_posted,datecreated,profile_picture FROM user_profile WHERE user_id = %s",[other_user_id])

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
                            no_of_tickets_posted = row[9]
                            datecreated = str(row[10].strftime('%Y-%m-%d %H:%M:%S'))
                            
                            date1 = datetime.strptime(str(datecreated), '%Y-%m-%d %H:%M:%S')
                            current_date = datetime.strptime(str(str(datetime.utcnow().date())), '%Y-%m-%d')
                            r = relativedelta.relativedelta(current_date, date1)
                            member_since = str(r.years) + " Years " + str(r.months) + " Months " + str(r.days) + " Days"
                            profile_picture = row[11]

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
                                    'no_of_tickets_posted': no_of_tickets_posted,
                                    'datecreated': datecreated,
                                    'member_since': member_since,
                                    'profile_picture': profile_picture
                                }
                        cursor.close()
                        connection.close()
                        
                        return Response(data)
                    else:
                        return Response({"response":"User does not exist OR Incorrect query params"})
                else:
                        return Response({"response":"Invalid User details"})
            else:
                        return Response({"response":"Incorrect Query parameters"})
        
        except Exception as e: 
            return Response({"response":"Error while getting profile info", "stacktrace":e.args[0]})


# EditProfile API
class EditProfile(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        try:
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

                is_image_upload = request.FILES['profile_picture'] if 'profile_picture' in request.FILES else False

                if is_image_upload == False:
                    path = ''
                else:
                    profile_picture = request.FILES['profile_picture']
                    actual_filename = request.FILES['profile_picture'].name
                    uploaded_filename = str(datetime.utcnow().strftime('%Y%m%d%H%M%S')) + "_" + actual_filename
                    uploaded_filepath = 'documents/profile_pictures/'+ str(datetime.utcnow().year) + '/' + str(datetime.utcnow().month) + '/' + str(datetime.utcnow().day) + '/' + uploaded_filename
                    path = default_storage.save(uploaded_filepath, ContentFile(profile_picture.read()))
                
                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])
                #cursor.execute("INSERT INTO user_profile(name,email,password,preference,profile_type,mobile,city,state,country,subscription_type,datecreated,dateupdated,auth_key) values(%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s) RETURNING user_id",[name, email, password, preference, profile_type, mobile, city, state, country, subscription_type, datecreated, dateupdated, auth_key])
                
                if cursor.rowcount >= 1:
                    cursor.execute("UPDATE user_profile SET name = %s, email = %s, preference = %s, profile_type = %s, mobile = %s, city = %s, state = %s, country = %s, subscription_type = %s, dateupdated = %s, profile_picture = %s WHERE user_id = %s RETURNING user_id",[name, email, preference, profile_type, mobile, city, state, country, subscription_type, dateupdated, path, user_id])
                    rows = cursor.fetchall()
                    for row in rows:
                        user_id = row[0]
                    data = {
                            'user_id': user_id
                            }
                    
                    cursor.close()
                    connection.close()

                    return Response(data)
                else:
                    return Response({"response":"Error while updating user info"})

        except Exception as e: 
            return Response({"response":"Error while updating user info", "stacktrace":e.args[0]})

# ChangePassword API
class ChangePassword(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        try:
            if request.method == "POST":
                user_id = request.data['user_id']
                auth_key = request.data['auth_key']
                old_password = request.data['old_password']
                password = request.data['password']

                dateupdated = str(datetime.utcnow())
                
                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])
                #cursor.execute("INSERT INTO user_profile(name,email,password,preference,profile_type,mobile,city,state,country,subscription_type,datecreated,dateupdated,auth_key) values(%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s , %s ,%s) RETURNING user_id",[name, email, password, preference, profile_type, mobile, city, state, country, subscription_type, datecreated, dateupdated, auth_key])
                
                if cursor.rowcount >= 1:
                    cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and password = %s",[user_id, old_password])
                    if cursor.rowcount >= 1:
                        cursor.execute("UPDATE user_profile SET password = %s, dateupdated = %s WHERE user_id = %s RETURNING user_id",[password,dateupdated,user_id])
                        rows = cursor.fetchall()
                        for row in rows:
                            user_id = row[0]
                        data = {
                                'user_id': user_id
                                }
                        
                        cursor.close()
                        connection.close()

                        return Response(data)
                    else:
                        return Response({"response":"Incorrect Old Password"})
                else:
                    return Response({"response":"Error while updating User Password"})
        
        except Exception as e:
            return Response({"response":"Error while Changing Password", "stacktrace":e.args[0]})
