from django.db.models import fields
from rest_framework import serializers
from movies.models import Movie, Actor, Crew, Review, Genre, Hashtag

# 전체 리스트를 보여주는 Serializer
class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'overview', 'poster_path')

# 상세 페이지를 보여주는 Serializer
class MovieSerializer(serializers.ModelSerializer):

    class ActorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = '__all__'
    
    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'
    
    class CrewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Crew
            fields = '__all__'
    
    class HashtagSerializer(serializers.ModelSerializer):
        class Meta:
            model = Hashtag
            fields = '__all__'

    actors = ActorSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    crews = CrewSerializer(many=True, read_only=True)
    keyword = HashtagSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'overview', 'release_date', 'genre',
        'vote_count', 'vote_average', 'actors', 'crews', 'keyword', 'poster_path', 'video_id')