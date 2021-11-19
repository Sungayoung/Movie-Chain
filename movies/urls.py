from django.urls import path
from . import views

app_name='movies'

urlpatterns = [
    path('', views.get_movie_list),
    path('search/', views.search),
    path('<int:movie_pk>/', views.get_movie_detail),
    path('<int:movie_pk>/actors/', views.get_actor_list),
    path('<int:movie_pk>/crews/', views.get_crew_list),
    path('<int:movie_pk>/reviews/', views.get_or_create_review),
    path('reviews/<int:review_pk>/', views.update_or_delete_review_or_get_or_create_comment_list),
    path('comments/<int:comment_pk>/', views.update_or_delete_comment),
    # path('save-movie/', views.index)
]
