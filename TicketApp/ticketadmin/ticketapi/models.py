from django.db import models
from django.db.models import DateTimeField

# Create your models here.
class TicketDetails(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    category = models.CharField(max_length = 100)
    subcategory = models.CharField(max_length = 100, blank=True, default='')
    product = models.CharField(max_length = 100, blank=True, default='')
    hashtag = models.CharField(max_length = 100,blank=True, default='')
    expiring_in_hours = models.CharField(max_length = 100, blank=True, default='')
    budget_in_rs = models.CharField(max_length = 100, blank=True, default='')
    addressline1 = models.CharField(max_length = 100, null=True, default='')
    city = models.CharField(max_length = 100, null=True, default='')
    state = models.CharField(max_length = 100, null=True, default='')
    pincode = models.CharField(max_length = 100, null=True, default='')
    country = models.CharField(max_length = 100, null=True, default='India')
    scope = models.CharField(max_length = 100, blank=True, default='Local') 
    ticket_description = models.CharField(max_length = 200, blank=True, default='') 
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ticket_details"