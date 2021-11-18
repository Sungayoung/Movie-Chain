from rest_framework import serializers
from accounts.models import User
from movies.models import Genre, Movie
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):

    profile_img = serializers.ImageField(use_url=True)

    class MovieListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('pk', 'title', 'overview', 'poster_path')

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'

    like_genres = GenreSerializer(many=True, read_only=True)
    personal_movies = MovieListSerializer(many=True, read_only=True)
    bookmark_movies = MovieListSerializer(many=True, read_only=True)
    favorite_movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'email', 'nickname', 'like_genres', 'personal_movies',
                  'bookmark_movies', 'favorite_movies', 'profile_img')


class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'nickname', 'password')
