from django.db.models import fields
from rest_framework import serializers
from .models import Query_Archived

class QueryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Query_Archived
        fields = '__all__' 

