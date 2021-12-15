from django.db import models
from datetime import date
# Create your models here.

class TwitterToken(models.Model):
    session_id = models.CharField(max_length=50, unique=True)
    oauth_token= models.CharField(max_length=150)
    oauth_secret= models.CharField(max_length=150)
    user_id= models.CharField(max_length=100)
    user_name= models.CharField(max_length=100)
