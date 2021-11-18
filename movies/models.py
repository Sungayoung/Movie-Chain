from django.db import models
from django.conf import settings
# Create your models here.

# 배우
class Actor(models.Model):
    id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    profile_path = models.TextField()

    def __str__(self):
        return f'[{self.id}]{self.name}'
    

# 장르
class Genre(models.Model):
    id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'[{self.id}]{self.name}'

# 제작진
class Crew(models.Model):
    id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    profile_path = models.TextField()

    def __str__(self):
        return f'[{self.id}]{self.name}'

# 해쉬태그
class Hashtag(models.Model):
    id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'[{self.id}]{self.name}'

# 영화
class Movie(models.Model):
    id = models.PositiveIntegerField()
    title = models.TextField()
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

    def __str__(self):
        return f'[{self.id}]{self.title}'

# 리뷰
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    rank = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')

    def __str__(self):
        return f'[{self.pk}]{self.user}'

# 리뷰댓글
class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'[{self.pk}]{self.user}'