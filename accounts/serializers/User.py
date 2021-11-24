from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from accounts.models import User
from movies.models import Genre, Movie
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):

    profile_img = serializers.ImageField(use_url=True)

    class MovieListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title', 'overview', 'poster_path', 'backdrop_path')

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'
    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        return obj.followers.filter(id=self.context.get('user').id).exists()

    like_genres = GenreSerializer(many=True, read_only=True)
    personal_movies = MovieListSerializer(many=True, read_only=True)
    bookmark_movies = MovieListSerializer(many=True, read_only=True)
    favorite_movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'like_genres', 'personal_movies', 'introduce_content',
                  'bookmark_movies', 'favorite_movies', 'profile_img', 'is_following', 'background_color')


class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    
    def validate_username(self, value):
        try:
            me = self.context.get('user')
            if User.objects.filter(username=value).exclude(id=me.id).exists():
                raise ValidationError('이미 등록된 ID 입니다.')
        except:
            if User.objects.filter(username=value).exists():
                raise ValidationError('이미 등록된 ID 입니다.')
        return value
    
    def validate_nickname(self, value):
        try:
            me = self.context.get('user')
            if User.objects.filter(nickname=value).exclude(id=me.id).exists():
                raise ValidationError('이미 등록된 닉네임입니다.')
        except:
            if User.objects.filter(nickname=value).exists():
                raise ValidationError('이미 등록된 닉네임입니다.')
        return value
    
    def validate_email(self, value):
        try:
            me = self.context.get('user')
            if User.objects.filter(email=value).exclude(id=me.id).exists():
                raise ValidationError('이미 등록된 이메일입니다.')
        except:
            if User.objects.filter(email=value).exists():
                raise ValidationError('이미 등록된 이메일입니다.')

        return value
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'nickname', 'password', 'birth', 'introduce_content')
