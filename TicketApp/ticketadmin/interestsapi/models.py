from django.db import models
from django.db.models import DateTimeField

# Create your models here.
class AllInterests(models.Model):
    intid = models.AutoField(primary_key=True)
    ticket_id = models.CharField(max_length = 100)
    user_id = models.CharField(max_length = 100)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "allinterests"