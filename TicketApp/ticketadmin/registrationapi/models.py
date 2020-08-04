from django.db import models
from django.db.models import DateTimeField

# Create your models here.
class UserProfile(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 35, default = '')
    email = models.CharField(max_length = 30, unique=True)
    password = models.CharField(max_length = 20)
    preference = models.CharField(max_length = 30)
    profile_type = models.CharField(max_length = 20)
    mobile = models.CharField(max_length = 13, unique=True)
    city = models.CharField(max_length = 25, blank=True, default='')
    state = models.CharField(max_length = 25, blank=True, default='')
    country = models.CharField(max_length = 25, blank=True, default='India')
    subscription_type = models.CharField(max_length = 20, blank=True, default='Free')
    auth_key = models.CharField(max_length = 40, blank=True, default='')
    no_of_tickets_posted = models.IntegerField(default=0)
    profile_picture = models.ImageField(blank=True, null=True,max_length = 300)
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profile"