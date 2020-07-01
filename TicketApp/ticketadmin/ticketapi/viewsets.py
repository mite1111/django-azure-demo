from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import status
from rest_framework.response import Response

class TicketDetailsViewSet(viewsets.ModelViewSet):
    queryset = models.ticketDetails.objects.all()
    serializer_class = serializers.ticketDetailsSerializer

    # def perform_create(self, serz):
    #     serz.save()

# class TicketDetailsViewSet(viewsets.ViewSet):

#     def list(self, request):
#         queryset = models.ticketDetails.objects.all()
#         serializer = serializers.ticketDetailsSerializer(queryset, many = True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = serializers.ticketDetailsSerializer(data=request.data)
#         if (request.data.get("Auth_Key") != "Woohoo"):
#             return Response("Incorrect Auth_Key", status=status.HTTP_400_BAD_REQUEST)

#         if serializer.is_valid():
#             serializer.save(creator=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        

    
    