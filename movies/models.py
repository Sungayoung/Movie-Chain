from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

# 배우
class Actor(models.Model):
    pk = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    profile_path = models.TextField()

# 장르
class Genre(models.Model):
    pk = models.PositiveIntegerField()
    name = models.CharField(max_length=100)

# 제작진
class Crew(models.Model):
    pk = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    profile_path = models.TextField()

# 해쉬태그
class Hashtag(models.Model):
    pk = models.PositiveIntegerField()
    name = models.CharField(max_length=100)

# 영화
class Movie(models.Model):
    pk = models.PositiveIntegerField()
    overview = models.TextField()
    release_date = models.DateField()
    genre = models.ManyToManyField(Genre, related_name='genre_movies')
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    actors = models.ManyToManyField(Actor, related_name='actor_movies')
    crews = models.ManyToManyField(Crew, related_name='crew_movies')
    keyword = models.ManyToManyField(Hashtag, related_name='hashtag_movies')
    poster_path = models.TextField()
    video_id = models.TextField()

# 리뷰
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    rank = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(get_user_model(), related_name='like_reviews')


# 리뷰댓글
class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.CharField(max_length=200)