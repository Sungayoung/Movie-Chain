from rest_framework import serializers
from movies.models import Actor


class ActorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Actor
        fields = ('pk', 'name', 'profile_path')
