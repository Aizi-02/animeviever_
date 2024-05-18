from django.urls import path
from .views import *

urlpatterns = [
    
    path('anime/<str:name>/<int:season_id>/<int:series_id>/', video_list, name='video_list'),
    path('', main_video_list, name='main_video_list'),
    path('anime_detail/<str:name>/', anime_detail, name='anime_detail'),
    path('search/', search_anime, name='search'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    
]