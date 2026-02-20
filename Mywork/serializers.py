from rest_framework import serializers
from .models import Labour, Site, WorkDetail

class LabourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labour
        fields = '__all__'

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

class WorkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDetail
        fields = '__all__'
