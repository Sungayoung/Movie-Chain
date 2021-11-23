from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name='accounts'

urlpatterns = [
    path('signup/', views.signup),
    path('update-user/', views.update_user),
    path('api-token-auth/', obtain_jwt_token),
    path('chatting/', views.chatting),
    path('profile/', views.get_or_set_profile_image),
    path('follow/', views.follow),
    path('set-personal-movie/', views.set_personal_movies)
]
