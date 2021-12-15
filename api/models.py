from django.db import models

from datetime import date

# Create your models here.
class Query_Archived(models.Model):
    query_string = models.TextField(max_length=1000)
    query_name = models.TextField(max_length=200, null=True)
    geo = models.BooleanField(default=0)
    date_created_at = models.DateField(default=date.today())