from django.contrib import admin
from .models import *


class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'profile_path',)
    list_display_links = ('id', 'name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)


class CrewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'job', 'profile_path', )
    list_display_links = ('id', 'name',)


class HashtagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'release_date',
                    'vote_count',
                    'vote_average',
                    'poster_path',
                    'video_id',)
    list_display_links = ('id', 'title',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'movie',
                    'user',
                    'content',
                    'rank',
                    'created_at',
                    'updated_at',)
    list_display_links = ('pk', 'movie',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'review',
                    'user',
                    'content',
                    'created_at',
                    'updated_at',)
    list_display_links = ('pk', 'review',)


admin.site.register(Actor, ActorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Crew, CrewAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
