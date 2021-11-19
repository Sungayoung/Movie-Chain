from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name='accounts'

urlpatterns = [
    path('signup/', views.signup),
    path('api-token-auth/', obtain_jwt_token),
<<<<<<< HEAD
    # path('chatting/', views.chatting),
=======
    path('chatting/', views.chatting),
    path('set-profile-image/', views.set_profile_image)
>>>>>>> 053e7dfb18e421ec97a9a7644ced8b1a2b799c5f
]
