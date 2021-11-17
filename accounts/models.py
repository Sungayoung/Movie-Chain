from django.db import models
from django.contrib.auth.models import AbstractUser
from ..movies.models import Movie, Genre


class User(AbstractUser):
    email = models.EmailField(blank=False)
    nickname = models.CharField(max_length=20)
    birth = models.DateField()
    profile_img = models.ImageField()
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followings')
    like_genres = models.ManyToManyField(Genre, related_name='genre_like_users')
    personal_movies = models.ManyToManyField(Movie, related_name='personal_movie_users')
    bookmark_movies = models.ManyToManyField(Movie, related_name='bookmark_users')
    favorite_movies = models.ManyToManyField(Movie, related_name='favorite_users')
