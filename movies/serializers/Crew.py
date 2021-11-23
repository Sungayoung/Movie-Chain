from rest_framework import serializers
from movies.models import Crew
from movies.serializers.Movie import MovieListSerializer


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ('id', 'name', 'job', 'profile_path')

class CrewProfileSerializer(serializers.ModelSerializer):

    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        return obj.acrew_following_user.filter(id=self.context.get('user').id).exists()
    
    crew_movies = MovieListSerializer(many=True)
    class Meta:
        model = Crew
        fields = ('id', 'name', 'job', 'profile_path', 'is_following')
