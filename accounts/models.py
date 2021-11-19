from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie, Genre, Actor, Crew


class User(AbstractUser):
    email = models.EmailField(blank=False)
    nickname = models.CharField(max_length=20)
    birth = models.DateField(null=True)
    profile_img = models.ImageField(null=True)
    introduce_content = models.CharField(max_length=200)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followings')
    blocked_user = models.ManyToManyField('self', symmetrical=False, related_name='blocking_user')
    to_chatting = models.ManyToManyField('self', symmetrical=False, through='Chatting', related_name='from_chatting')
    actor_following = models.ManyToManyField()
    like_genres = models.ManyToManyField(Genre, related_name='genre_like_users')
    personal_movies = models.ManyToManyField(Movie, related_name='personal_movie_users')
    bookmark_movies = models.ManyToManyField(Movie, related_name='bookmark_users')
    favorite_movies = models.ManyToManyField(Movie, related_name='favorite_users')


class Chatting(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)