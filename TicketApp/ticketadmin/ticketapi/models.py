from django.db import models
from django.db.models import DateTimeField

# Create your models here.
class ticketDetails(models.Model):
    Category = models.CharField(max_length = 100)
    SubCategory = models.CharField(max_length = 100)
    Product = models.CharField(max_length = 100)
    HashTag = models.CharField(max_length = 100)
    ExpiringInHours = models.CharField(max_length = 100)
    BudgetPriceInRs = models.CharField(max_length = 100)
    DateCreated = models.DateField()
    DateUpdated = models.DateField()