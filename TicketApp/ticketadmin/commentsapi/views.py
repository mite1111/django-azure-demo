from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AllCommentsSerializer
from django.db import connection
from django.http import HttpResponse
import random
import json
import uuid
from datetime import datetime
from django.http import JsonResponse
import collections

#PostComment API
class PostCommentAPI(generics.GenericAPIView):
    serializer_class = AllCommentsSerializer

    def post(self, request):
        if request.method == "POST":
            user_id = request.data['user_id']
            auth_key = request.data['auth_key']
            
            ticket_id = request.data['ticket_id']
            comment_text = request.data['comment_text']
            dateupdated = str(datetime.utcnow())
            
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])
            
            if cursor.rowcount >= 1:
                cursor.execute("INSERT INTO allcomments(ticket_id,user_id,comment_text,dateupdated) values(%s , %s ,%s , %s) RETURNING cid",[ticket_id, user_id,comment_text,dateupdated])
                rows = cursor.fetchall()
                for row in rows:
                    cid = row[0]
                data = {
                        'cid': cid
                        }
                return Response(data)
            else:
                return Response({"response":"Error saving comments"})


#GetCommentsByUserId API
class GetCommentsByUserId(APIView):
    # serializer_class = PostTicketSerializer
    
    def get(self, request):
        if request.GET.get('user_id') and request.GET.get('name') and request.GET.get('auth_key'):
            user_id = request.GET.get('user_id')
            auth_key = request.GET.get('auth_key')

            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s and auth_key = %s",[user_id, auth_key])

            if cursor.rowcount >= 1:
                cursor.execute("SELECT cid,ticket_id,user_id,comment_text,dateupdated FROM allcomments WHERE user_id = %s",[user_id])
                rows = cursor.fetchall()
                rowarray_list = []
                for row in rows:
                    t = (row[0], row[1], row[2], row[3], str(row[4]))
                    rowarray_list.append(t)
                j = json.dumps(rowarray_list)
                
                # Convert query to objects of key-value pairs
                objects_list = []
                for row in rows:
                    d = collections.OrderedDict()
                    d['cid'] = row[0]
                    d['ticket_id'] = row[1]
                    d['user_id'] = row[2]
                    d['comment_text'] = row[3]
                    d['dateupdated'] = str(row[4])
                    objects_list.append(d)

                j = json.dumps(objects_list)
                return HttpResponse(j, content_type = "application/json")
            else:
                return Response({"response":"User does not exist OR Incorrect query params"})
        else:
                return Response({"response":"Incorrect number of Query parameters"})


#GetCommentsByTicketId API
class GetCommentsByTicketId(APIView):
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
                cursor.execute("SELECT cid,ticket_id,user_id,comment_text,dateupdated FROM allcomments WHERE ticket_id = %s",[ticket_id])
                rows = cursor.fetchall()
                rowarray_list = []
                for row in rows:
                    t = (row[0], row[1], row[2], row[3], str(row[4]))
                    rowarray_list.append(t)
                j = json.dumps(rowarray_list)
                
                # Convert query to objects of key-value pairs
                objects_list = []
                for row in rows:
                    d = collections.OrderedDict()
                    d['cid'] = row[0]
                    d['ticket_id'] = row[1]
                    d['user_id'] = row[2]
                    d['comment_text'] = row[3]
                    d['dateupdated'] = str(row[4])
                    objects_list.append(d)

                j = json.dumps(objects_list)
                return HttpResponse(j, content_type = "application/json")
            else:
                return Response({"response":"User does not exist OR Incorrect query params"})
        else:
                return Response({"response":"Incorrect number of Query parameters"})

