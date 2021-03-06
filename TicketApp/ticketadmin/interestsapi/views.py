from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AllInterestsSerializer
from django.db import connection
from django.http import HttpResponse
import random
import json
import uuid
from datetime import datetime
from django.http import JsonResponse
import collections

#PostInterest API
class PostInterestAPI(generics.GenericAPIView):
    serializer_class = AllInterestsSerializer

    def post(self, request):
        try:
            if request.method == "POST":
                user_id = request.data['user_id']
                auth_key = request.data['auth_key']
                
                ticket_id = request.data['ticket_id']
                dateupdated = str(datetime.utcnow())
                
                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])
                
                if cursor.rowcount >= 1:
                    cursor.execute("SELECT intid FROM allinterests WHERE user_id = %s and ticket_id = %s",[user_id, ticket_id])
                    if cursor.rowcount == 0:
                        cursor.execute("UPDATE ticket_Details SET interests_count = (interests_count + 1) WHERE ticket_id = %s",[ticket_id])
                        cursor.execute("INSERT INTO allinterests(ticket_id,user_id,dateupdated) values(%s , %s ,%s) RETURNING intid",[ticket_id, user_id,dateupdated])
                        rows = cursor.fetchall()
                        for row in rows:
                            intid = row[0]
                        data = {
                                'intid': intid
                                }
                        cursor.close()
                        connection.close()

                        return Response(data)
                    else:
                        return Response({"response":"Interest record already exists for ticket_id and user_id combination"})
                else:
                    return Response({"response":"Error saving interest"})
        
        except Exception as e: 
            return Response({"response":"Error while saving Interest", "stacktrace":e.args[0]})


#GetInterestsByUserid API
class GetInterestsByUserid(APIView):
    # serializer_class = PostTicketSerializer
    
    def get(self, request):
        try:
            if request.GET.get('user_id') and request.GET.get('name') and request.GET.get('auth_key'):
                user_id = request.GET.get('user_id')
                auth_key = request.GET.get('auth_key')

                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])

                if cursor.rowcount >= 1:
                    cursor.execute("SELECT intid,ticket_id,user_id,dateupdated FROM allinterests WHERE user_id = %s",[user_id])
                    rows = cursor.fetchall()
                    rowarray_list = []
                    for row in rows:
                        t = (row[0], row[1], row[2], str(row[3]))
                        rowarray_list.append(t)
                    j = json.dumps(rowarray_list)
                    
                    # Convert query to objects of key-value pairs
                    objects_list = []
                    for row in rows:
                        d = collections.OrderedDict()
                        d['intid'] = row[0]
                        d['ticket_id'] = row[1]
                        d['user_id'] = row[2]
                        d['dateupdated'] = str(row[3].strftime('%Y-%m-%d %H:%M:%S'))
                        objects_list.append(d)

                    j = json.dumps(objects_list)
                    cursor.close()
                    connection.close()
                    return HttpResponse(j, content_type = "application/json")
                else:
                    return Response({"response":"User does not exist OR Incorrect query params"})
            else:
                    return Response({"response":"Incorrect number of Query parameters"})
    
        except Exception as e: 
            return Response({"response":"Error while fetching Interest", "stacktrace":e.args[0]})


#GetInterestsByTicketId API
class GetInterestsByTicketId(APIView):
    # serializer_class = PostTicketSerializer
    
    def get(self, request):
        try:
            if request.GET.get('user_id') and request.GET.get('name') and request.GET.get('auth_key') and request.GET.get('ticket_id'):
                user_id = request.GET.get('user_id')
                # name = request.GET.get('name')
                auth_key = request.GET.get('auth_key')
                ticket_id = request.GET.get('ticket_id')

                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])

                if cursor.rowcount >= 1:
                    cursor.execute("SELECT ai.intid, ai.ticket_id, ai.user_id, ai.dateupdated, up.name FROM allinterests ai INNER JOIN user_profile up on ai.user_id = up.user_id WHERE ticket_id = %s",[ticket_id])
                    rows = cursor.fetchall()
                    rowarray_list = []
                    for row in rows:
                        t = (row[0], row[1], row[2],str(row[3]),row[4])
                        rowarray_list.append(t)
                    j = json.dumps(rowarray_list)
                    
                    # Convert query to objects of key-value pairs
                    objects_list = []
                    for row in rows:
                        d = collections.OrderedDict()
                        d['intid'] = row[0]
                        d['ticket_id'] = row[1]
                        d['user_id'] = row[2]
                        d['dateupdated'] = str(row[3].strftime('%Y-%m-%d %H:%M:%S'))
                        d['name'] = row[4]
                        objects_list.append(d)

                    j = json.dumps(objects_list)
                    cursor.close()
                    connection.close()
                    return HttpResponse(j, content_type = "application/json")
                else:
                    return Response({"response":"User does not exist OR Incorrect query params"})
            else:
                    return Response({"response":"Incorrect number of Query parameters"})
        
        except Exception as e: 
            return Response({"response":"Error while fetching Interest", "stacktrace":e.args[0]})

#RemoveInterestByTicketId API
class RemoveInterestByTicketId(generics.GenericAPIView):
    serializer_class = AllInterestsSerializer
    
    def post(self, request):
        try:
            if request.method == "POST":
                user_id = request.data['user_id']
                auth_key = request.data['auth_key']
                
                ticket_id = request.data['ticket_id']
                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])
                
                if cursor.rowcount >= 1:
                    cursor.execute("SELECT user_id FROM allinterests WHERE user_id = %s and ticket_id = %s",[user_id, ticket_id])
                    if cursor.rowcount >= 1:
                        cursor.execute("DELETE FROM allinterests WHERE user_id = %s and ticket_id = %s",[user_id, ticket_id])
                        cursor.execute("UPDATE ticket_Details SET interests_count = (interests_count - 1) WHERE ticket_id = %s",[ticket_id])
                    
                        data = {
                                'ticket_id': ticket_id,
                                'response': 'Interest removed successfully'
                                }
                        
                        cursor.close()
                        connection.close()
                        return Response(data)
                    else:
                        return Response({"response":"Interest not found for given user_id and ticket_id combination"})
                else:
                    return Response({"response":"Error removing interest"})
        
        except Exception as e: 
            return Response({"response":"Error while Removing Interest", "stacktrace":e.args[0]})

