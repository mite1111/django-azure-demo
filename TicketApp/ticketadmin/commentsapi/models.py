from django.db import models
from django.db.models import DateTimeField

# Create your models here.
class AllComments(models.Model):
    cid = models.AutoField(primary_key=True)
    ticket_id = models.IntegerField()
    user_id = models.IntegerField()
    comment_text = models.CharField(max_length = 200,blank=True, default='')
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "allcomments"