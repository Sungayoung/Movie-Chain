from django.db.models import fields
from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from movies.models import Movie, Actor, Crew, Review, Genre, Hashtag, CharacterName
from accounts.models import User

# 전체 리스트를 보여주는 Serializer
class MovieListSerializer(serializers.ModelSerializer):
    isLiked = serializers.SerializerMethodField()
    isSaved = serializers.SerializerMethodField()
    def get_isLiked(self, obj):
        try:
            return obj.favorite_users.filter(id=self.context.get('user').id).exists()
        except:
            return False
    
    def get_isSaved(self, obj):
        try:
            return obj.bookmark_users.filter(id=self.context.get('user').id).exists()
        except:
            return False

    class Meta:
        model = Movie
        fields = ('id', 'title', 'overview', 'poster_path', 'backdrop_path', 'isLiked', 'isSaved')

# 상세 페이지를 보여주는 Serializer
class MovieSerializer(serializers.ModelSerializer):
    
    class ActorSerializer(serializers.ModelSerializer):

        character = serializers.SerializerMethodField()
        def get_character(self, obj):
            return obj.actor_movies.through.objects.filter(actor=obj, movie=self.context.get('movie'))[0].character
        
        class Meta:
            model = Actor
            fields = ('id', 'name', 'profile_path', 'birthday', 'deathday', 'homepage', 'character')
    
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
    
    actors = serializers.SerializerMethodField()

    isLiked = serializers.SerializerMethodField()
    isSaved = serializers.SerializerMethodField()
    likeCnt = serializers.SerializerMethodField()
    saveCnt = serializers.SerializerMethodField()
    background_color = serializers.SerializerMethodField()
    def get_actors(self, obj):
        actors = self.ActorSerializer(obj.actors, many=True, read_only=True, context={'movie': obj})
        return actors.data
    genre = GenreSerializer(many=True, read_only=True)
    crews = CrewSerializer(many=True, read_only=True)
    keyword = HashtagSerializer(many=True, read_only=True)
    def get_likeCnt(self, obj):
        return obj.favorite_users.count()

    def get_saveCnt(self, obj):
        return obj.bookmark_users.count()

    def get_isLiked(self, obj):
        return obj.favorite_users.filter(id=self.context.get('user').id).exists()
    
    def get_isSaved(self, obj):
        return obj.bookmark_users.filter(id=self.context.get('user').id).exists()
    
    def get_background_color(self, obj):
        return self.context.get('user').background_color
    
    class Meta:
        model = Movie
        fields = ('id', 'title', 'overview', 'release_date', 'genre', 'likeCnt', 'saveCnt', 'backdrop_path',
        'vote_count', 'vote_average', 'actors', 'crews', 'keyword', 'poster_path', 'video_id', 'isLiked', 'isSaved', 'background_color')