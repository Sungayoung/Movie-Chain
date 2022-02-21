from rest_framework import serializers
from movies.models import Actor
from movies.serializers.Movie import MovieListSerializer


class ActorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Actor
        fields = ('id', 'name', 'profile_path')

class ActorProfileSerializer(serializers.ModelSerializer):
    
    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        return obj.actor_following_user.filter(id=self.context.get('user').id).exists()
    
    movies = MovieListSerializer(source='actor_movies', many=True)
    class Meta:
        model = Actor
        fields = ('id', 'name', 'profile_path', 'is_following', 'birthday', 'deathday', 'homepage', 'movies')
