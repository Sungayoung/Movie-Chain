from typing import runtime_checkable
from django.core.files import storage
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.contrib.auth.models import AbstractUser
from movies.models import Movie, Genre, Actor, Crew
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

def profile_image_path(instance, filename):
    return f'images/profile/{instance.id}/{instance.id}.jpg'

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name: str, max_length: None) -> str:
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class User(AbstractUser):
    email = models.EmailField(blank=False)
    nickname = models.CharField(max_length=20, unique=True)
    birth = models.DateField(null=True)
    profile_img = ProcessedImageField(
        default='images/profile/default.jpg',
        processors=[Thumbnail(300, 300)],
        format="JPEG",
        options={'quality': 90},
        upload_to=profile_image_path,
        storage=OverwriteStorage()
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
    is_read = models.BooleanField(default=False)