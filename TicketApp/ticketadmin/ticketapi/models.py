from django.db import models
from django.db.models import DateTimeField

# Create your models here.
class TicketDetails(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    category = models.CharField(max_length = 100)
    subcategory = models.CharField(max_length = 100, blank=True, default='')
    product = models.CharField(max_length = 100, blank=True, default='')
    # hashtag = models.CharField(max_length = 100,blank=True, default='')
    expiring_in_hours = models.CharField(max_length = 100, blank=True, default='')
    budget_in_rs = models.CharField(max_length = 100, blank=True, default='')
    addressline1 = models.CharField(max_length = 100, null=True, default='')
    city = models.CharField(max_length = 100, null=True, default='')
    state = models.CharField(max_length = 100, null=True, default='')
    pincode = models.CharField(max_length = 100, null=True, default='')
    country = models.CharField(max_length = 100, null=True, default='India')
    scope = models.CharField(max_length = 100, blank=True, default='Local') 
    ticket_description = models.CharField(max_length = 200, blank=True, default='')
    interests_count = models.IntegerField(default=0)
    ticket_type = models.CharField(max_length = 20, blank=True, default='')
    ticket_picture = models.ImageField(blank=True, null=True,max_length = 300)
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ticket_details"

class HashtagMaster(models.Model):
    hashtag_id = models.AutoField(primary_key=True)
    hashtag = models.CharField(max_length = 50)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hashtag_master"

class TicketHashtag(models.Model):
    id = models.AutoField(primary_key=True)
    hashtag_id = models.IntegerField()
    ticket_id = models.IntegerField()
    user_id = models.IntegerField()
    hashtag = models.CharField(max_length = 50)
    active = models.IntegerField()
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ticket_hashtag"