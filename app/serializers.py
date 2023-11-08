from .models import Campana
from rest_framework import serializers

class CampanaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campana
        fields = '__all__'
        
        