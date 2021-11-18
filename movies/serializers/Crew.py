from rest_framework import serializers
from movies.models import Crew


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ('id', 'name', 'job', 'profile_path')
