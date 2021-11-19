from typing import runtime_checkable
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.contrib.auth.models import AbstractUser
from movies.models import Movie, Genre, Actor, Crew

def profile_image_path(instance, filename):
    return f'images/profile/{instance.id}'

class User(AbstractUser):
    email = models.EmailField(blank=False)
    nickname = models.CharField(max_length=20)
    birth = models.DateField(null=True)
    profile_img = ProcessedImageField(
        null=True,
        processors=[Thumbnail(300, 400)],
        format="JPEG",
        options={'quality': 90},
        upload_to=profile_image_path
    )
    introduce_content = models.CharField(max_length=200, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followings')
    blocked_user = models.ManyToManyField('self', symmetrical=False, related_name='blocking_user')
    to_chatting = models.ManyToManyField('self', symmetrical=False, through='Chatting', related_name='from_chatting')
    actor_following = models.ManyToManyField(Actor, related_name='actor_following_user')
    crew_following = models.ManyToManyField(Crew, related_name='crew_following_user')
    like_genres = models.ManyToManyField(Genre, related_name='genre_like_users')
    personal_movies = models.ManyToManyField(Movie, related_name='personal_movie_users')
    bookmark_movies = models.ManyToManyField(Movie, related_name='bookmark_users')
    favorite_movies = models.ManyToManyField(Movie, related_name='favorite_users')


class Chatting(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_to_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_from_user")
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)