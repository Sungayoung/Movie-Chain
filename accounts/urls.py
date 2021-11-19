from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name='accounts'

urlpatterns = [
    path('signup/', views.signup),
    path('api-token-auth/', obtain_jwt_token),
    path('chatting/', views.chatting),
<<<<<<< HEAD
    path('set-profile-image/', views.set_profile_image)
=======
    path('profile/', views.get_or_set_profile_image),
>>>>>>> 0ad159edac69c7f3d8b7133ac10afd580bfa1d02
]
