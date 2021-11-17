from rest_framework import serializers
from ..models import Crew


class CrewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Crew
        fields = ('pk', 'name', 'job', 'profile_path')
