from django.urls import path
from . import views

app_name='movies'

urlpatterns = [
    path('', views.get_movie_list),
    path('page/', views.get_movie_list_page),
    path('search/', views.search),
    path('<int:movie_pk>/', views.get_movie_detail),
    path('people/<int:people_pk>/', views.get_people_detail),
    path('<int:movie_pk>/actors/', views.get_actor_list),
    path('<int:movie_pk>/crews/', views.get_crew_list),
    path('actors/', views.get_actor_list_all),
    path('crews/', views.get_crew_list_all),
    path('genres/', views.get_genre_list_all),
    path('hashtags/', views.get_hashtag_list_all),
    path('<int:movie_pk>/reviews/', views.get_or_create_review),
    path('reviews/<int:review_pk>/', views.update_or_delete_review_or_get_or_create_comment_list),
    path('comments/<int:comment_pk>/', views.update_or_delete_comment),
    path('like-movie/', views.like_movie),
    path('bookmark-movie/', views.bookmark_movie),
    path('like-review/', views.like_review)
    # path('save-movie/', views.index)
]
