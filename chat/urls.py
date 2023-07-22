from django.urls import path
from . import views


urlpatterns = [
    path('home/',views.home, name="home"),
    path('', views.text_to_mp3, name='text_to_mp3'),    path('/text_to_mp3/', views.text_to_mp3, name='text_to_mp3'),    
]
