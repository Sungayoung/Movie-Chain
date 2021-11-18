from rest_framework import serializers
from movies.models import Actor


class ActorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Actor
        fields = ('id', 'name', 'profile_path')
