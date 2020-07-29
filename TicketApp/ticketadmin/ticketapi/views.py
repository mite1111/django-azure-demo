from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostTicketSerializer, EditTicketSerializer
from django.db import connection
from django.http import HttpResponse
import random
import json
import uuid
from datetime import datetime
from django.http import JsonResponse
import collections

#PostTicket API
class PostTicketAPI(generics.GenericAPIView):
    serializer_class = PostTicketSerializer

    def post(self, request):
        if request.method == "POST":
            user_id = request.data['user_id']
            auth_key = request.data['auth_key']
            
            category = request.data['category']
            subcategory = request.data['subcategory']
            product = request.data['product']
            # hashtag = ''
            expiring_in_hours = request.data['expiring_in_hours']
            budget_in_rs = request.data['budget_in_rs']
            scope = request.data['scope']
            ticket_description = request.data['ticket_description']
            interests_count = 0
            datecreated = str(datetime.utcnow())
            dateupdated = str(datetime.utcnow())
            
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])
            
            if cursor.rowcount >= 1:
                cursor.execute("INSERT INTO ticket_Details(category,subcategory,product,expiring_in_hours,budget_in_rs,scope,ticket_description,user_id,datecreated,dateupdated,interests_count) values(%s , %s , %s ,%s , %s ,%s , %s ,%s , %s ,%s, %s) RETURNING ticket_id",[category,subcategory,product,expiring_in_hours,budget_in_rs,scope,ticket_description,user_id,datecreated,dateupdated,interests_count])
                rows = cursor.fetchall()
                for row in rows:
                    ticket_id = row[0]
                for element in request.data['hashtag']:
                    cursor.execute("SELECT hashtag_id, hashtag FROM hashtag_master WHERE hashtag = %s",[element['hashtag']])
                    if cursor.rowcount >= 1:
                        rows = cursor.fetchall()
                        for row in rows:
                            cursor.execute("INSERT INTO ticket_hashtag(hashtag_id,ticket_id,user_id,hashtag,active,dateupdated) VALUES(%s , %s ,%s , %s, %s, %s)",[row[0],ticket_id,user_id,row[1],1,dateupdated])
                    else:
                        cursor.execute("INSERT INTO hashtag_master(hashtag,dateupdated) VALUES(%s, %s) RETURNING hashtag_id, hashtag",[element['hashtag'],dateupdated])
                        rows = cursor.fetchall()
                        for row in rows:
                            cursor.execute("INSERT INTO ticket_hashtag(hashtag_id,ticket_id,user_id,hashtag,active,dateupdated) VALUES(%s , %s ,%s , %s, %s, %s)",[row[0],ticket_id,user_id,row[1],1,dateupdated])
                data = {
                        'ticket_id': ticket_id
                        }
                return Response(data)
            else:
                return Response({"response":"Error saving ticket info"})


#GetMyTickets API
class GetMyTicketsAPI(APIView):
    # serializer_class = PostTicketSerializer
    
    def get(self, request):
        if request.GET.get('user_id') and request.GET.get('name') and request.GET.get('auth_key'):
            user_id = request.GET.get('user_id')
            # name = request.GET.get('name')
            auth_key = request.GET.get('auth_key')

            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])

            if cursor.rowcount >= 1:
                cursor.execute("SELECT ticket_id,category,subcategory,product,expiring_in_hours,budget_in_rs,scope,ticket_description,datecreated,interests_count FROM ticket_details WHERE user_id = %s",[user_id])
                rows = cursor.fetchall()
                rowarray_list = []
                for row in rows:
                    t = (str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], str(row[8]),row[9])
                    rowarray_list.append(t)
                j = json.dumps(rowarray_list)
                
                # Convert query to objects of key-value pairs
                objects_list = []
                for row in rows:
                    d = collections.OrderedDict()
                    d['ticket_id'] = str(row[0])
                    d['category'] = row[1]
                    d['subcategory'] = row[2]
                    d['product'] = row[3]
                    cursor.execute("SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(t))) FROM (SELECT hashtag FROM ticket_hashtag WHERE ticket_id = %s AND active = 1) t",[row[0]])
                    ht = cursor.fetchall()
                    d['hashtag'] = ht[0][0]
                    d['expiring_in_hours'] = row[4]
                    d['budget_in_rs'] = row[5]
                    d['scope'] = row[6]
                    d['ticket_description'] = row[7]
                    d['datecreated'] = str(row[8].strftime('%Y-%m-%d %H:%M:%S'))
                    d['interests_count'] = row[9]
                    
                    objects_list.append(d)

                j = json.dumps(objects_list)
                return HttpResponse(j, content_type = "application/json")
            else:
                return Response({"response":"User does not exist OR Incorrect query params"})
        else:
                return Response({"response":"Incorrect number of Query parameters"})


#GetTicketById API
class GetTicketById(APIView):
    # serializer_class = PostTicketSerializer
    
    def get(self, request):
        if request.GET.get('user_id') and request.GET.get('name') and request.GET.get('auth_key') and request.GET.get('ticket_id'):
            user_id = request.GET.get('user_id')
            # name = request.GET.get('name')
            auth_key = request.GET.get('auth_key')
            ticket_id = request.GET.get('ticket_id')

            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])

            if cursor.rowcount >= 1:
                cursor.execute("SELECT ticket_id,category,subcategory,product,expiring_in_hours,budget_in_rs,scope,ticket_description,datecreated,interests_count FROM ticket_details WHERE ticket_id = %s",[ticket_id])
                rows = cursor.fetchall()
                rowarray_list = []
                for row in rows:
                    t = (str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], str(row[8]),row[9])
                    rowarray_list.append(t)
                j = json.dumps(rowarray_list)
                
                # Convert query to objects of key-value pairs
                objects_list = []
                for row in rows:
                    d = collections.OrderedDict()
                    d['ticket_id'] = str(row[0])
                    d['category'] = row[1]
                    d['subcategory'] = row[2]
                    d['product'] = row[3]
                    cursor.execute("SELECT ARRAY_TO_JSON(ARRAY_AGG(row_to_json(t))) FROM (SELECT hashtag FROM ticket_hashtag WHERE ticket_id = %s AND active = 1) t",[row[0]])
                    ht = cursor.fetchall()
                    d['hashtag'] = ht[0][0]
                    d['expiring_in_hours'] = row[4]
                    d['budget_in_rs'] = row[5]
                    d['scope'] = row[6]
                    d['ticket_description'] = row[7]
                    d['datecreated'] = str(row[8].strftime('%Y-%m-%d %H:%M:%S'))
                    d['interests_count'] = row[9]
                    
                    objects_list.append(d)

                j = json.dumps(objects_list)
                return HttpResponse(j, content_type = "application/json")
            else:
                return Response({"response":"User does not exist OR Incorrect query params"})
        else:
                return Response({"response":"Incorrect number of Query parameters"})

#GetTicketById API
class GetTicketByHashtag(APIView):
    # serializer_class = PostTicketSerializer
    
    def get(self, request):
        if request.GET.get('user_id') and request.GET.get('name') and request.GET.get('auth_key') and request.GET.get('hashtag'):
            user_id = request.GET.get('user_id')
            # name = request.GET.get('name')
            auth_key = request.GET.get('auth_key')
            hashtag = request.GET.get('hashtag')

            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])

            if cursor.rowcount >= 1:
                cursor.execute("SELECT tc.ticket_id,tc.category,tc.subcategory,tc.product,ht.hashtag,tc.expiring_in_hours,tc.budget_in_rs,tc.scope,tc.ticket_description,tc.datecreated,tc.interests_count FROM ticket_details tc JOIN ticket_hashtag ht ON tc.ticket_id = ht.ticket_id WHERE ht.hashtag = %s AND ht.active = 1 ORDER BY tc.ticket_id DESC",[hashtag])
                rows = cursor.fetchall()
                rowarray_list = []
                for row in rows:
                    t = (str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],str(row[9]),row[10])
                    rowarray_list.append(t)
                j = json.dumps(rowarray_list)
                
                # Convert query to objects of key-value pairs
                objects_list = []
                for row in rows:
                    d = collections.OrderedDict()
                    d['ticket_id'] = str(row[0])
                    d['category'] = row[1]
                    d['subcategory'] = row[2]
                    d['product'] = row[3]
                    d['hashtag'] = row[4]
                    d['expiring_in_hours'] = row[5]
                    d['budget_in_rs'] = row[6]
                    d['scope'] = row[7]
                    d['ticket_description'] = row[8]
                    d['datecreated'] = str(row[9].strftime('%Y-%m-%d %H:%M:%S'))
                    d['interests_count'] = row[10]
                    
                    objects_list.append(d)

                j = json.dumps(objects_list)
                return HttpResponse(j, content_type = "application/json")
            else:
                return Response({"response":"User does not exist OR Incorrect query params"})
        else:
                return Response({"response":"Incorrect number of Query parameters"})

#GetFewTicketByHashtag API
class GetFewTicketByHashtag(APIView):
    # serializer_class = PostTicketSerializer
    
    def get(self, request):
        if request.GET.get('user_id') and request.GET.get('name') and request.GET.get('auth_key') and request.GET.get('hashtag'):
            user_id = request.GET.get('user_id')
            # name = request.GET.get('name')
            auth_key = request.GET.get('auth_key')
            hashtag = request.GET.get('hashtag')

            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])

            if cursor.rowcount >= 1:
                cursor.execute("SELECT tc.ticket_id,tc.category,tc.subcategory,tc.product,ht.hashtag,tc.expiring_in_hours,tc.budget_in_rs,tc.scope,tc.ticket_description,tc.datecreated,tc.interests_count FROM ticket_details tc JOIN ticket_hashtag ht ON tc.ticket_id = ht.ticket_id WHERE ht.hashtag = %s ORDER BY tc.ticket_id DESC LIMIT 10",[hashtag])
                rows = cursor.fetchall()
                rowarray_list = []
                for row in rows:
                    t = (str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],str(row[9]),row[10])
                    rowarray_list.append(t)
                j = json.dumps(rowarray_list)
                
                # Convert query to objects of key-value pairs
                objects_list = []
                for row in rows:
                    d = collections.OrderedDict()
                    d['ticket_id'] = str(row[0])
                    d['category'] = row[1]
                    d['subcategory'] = row[2]
                    d['product'] = row[3]
                    d['hashtag'] = row[4]
                    d['expiring_in_hours'] = row[5]
                    d['budget_in_rs'] = row[6]
                    d['scope'] = row[7]
                    d['ticket_description'] = row[8]
                    d['datecreated'] = str(row[9].strftime('%Y-%m-%d %H:%M:%S'))
                    d['interests_count'] = row[10]
                    
                    objects_list.append(d)

                j = json.dumps(objects_list)
                return HttpResponse(j, content_type = "application/json")
            else:
                return Response({"response":"User does not exist OR Incorrect query params"})
        else:
                return Response({"response":"Incorrect number of Query parameters"})


#EditTicket API
class EditTicketAPI(generics.GenericAPIView):
    serializer_class = EditTicketSerializer

    def post(self, request):
        if request.method == "POST":
            user_id = request.data['user_id']
            auth_key = request.data['auth_key']
            
            ticket_id = request.data['ticket_id']
            category = request.data['category']
            subcategory = request.data['subcategory']
            product = request.data['product']
            # hashtag = ''
            budget_in_rs = request.data['budget_in_rs']
            scope = request.data['scope']
            ticket_description = request.data['ticket_description']
            dateupdated = str(datetime.utcnow())

            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])
            
            if cursor.rowcount >= 1:
                cursor.execute("UPDATE ticket_Details SET category = %s, subcategory = %s, product = %s, budget_in_rs = %s, scope = %s, ticket_description = %s, dateupdated = %s WHERE user_id = %s AND ticket_id = %s RETURNING ticket_id",[category, subcategory, product, budget_in_rs, scope, ticket_description, dateupdated, user_id, ticket_id])
                rows = cursor.fetchall()
                for row in rows:
                    ticket_id = row[0]
                # for element in request.data['hashtag']:
                #     cursor.execute("SELECT hashtag_id, hashtag FROM hashtag_master WHERE hashtag = %s",[element['hashtag']])
                #     if cursor.rowcount >= 1:
                #         rows = cursor.fetchall()
                #         for row in rows:
                #             cursor.execute("INSERT INTO ticket_hashtag(hashtag_id,ticket_id,user_id,hashtag,active,dateupdated) VALUES(%s , %s ,%s , %s, %s, %s)",[row[0],ticket_id,user_id,row[1],1,dateupdated])
                #     else:
                #         cursor.execute("INSERT INTO hashtag_master(hashtag,dateupdated) VALUES(%s, %s) RETURNING hashtag_id, hashtag",[element['hashtag'],dateupdated])
                #         rows = cursor.fetchall()
                #         for row in rows:
                #             cursor.execute("INSERT INTO ticket_hashtag(hashtag_id,ticket_id,user_id,hashtag,active,dateupdated) VALUES(%s , %s ,%s , %s, %s, %s)",[row[0],ticket_id,user_id,row[1],1,dateupdated])
                data = {
                        'ticket_id': ticket_id
                        }
                return Response(data)
            else:
                return Response({"response":"Error while updating ticket info"})

