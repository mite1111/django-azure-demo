from django.db import models
from django.db.models import DateTimeField

# Create your models here.
class ticketDetails(models.Model):
    Auth_Key = models.CharField(max_length = 100)
    TicketId = models.AutoField(primary_key=True)
    Category = models.CharField(max_length = 100)
    SubCategory = models.CharField(max_length = 100)
    Product = models.CharField(max_length = 100)
    HashTag = models.CharField(max_length = 100)
    ExpiringInHours = models.CharField(max_length = 100)
    BudgetPriceInRs = models.CharField(max_length = 100)
    AddressLine1 = models.CharField(max_length = 100)
    AddressLine2 = models.CharField(max_length = 100)
    City = models.CharField(max_length = 100)
    State = models.CharField(max_length = 100)
    PinCode = models.CharField(max_length = 100)
    DateCreated = models.DateTimeField(auto_now_add=True)
    DateUpdated = models.DateTimeField(auto_now=True)
    
class auth(models.Model):
    Auth_Key = models.CharField(max_length = 100)