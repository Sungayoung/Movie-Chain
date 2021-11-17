from rest_framework import serializers
from ..models import Actor


class ActorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Actor
        fields = ('pk', 'name', 'profile_path')
