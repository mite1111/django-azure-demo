from rest_framework import viewsets
from . import models
from . import serializers

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = models.AllComments.objects.all()
    serializer_class = serializers.AllCommentsSerializer
