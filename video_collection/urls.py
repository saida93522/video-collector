""" Handles all of the specific url routes,queries from db or templates that need to be rendered.links specific URL(urlpath) to the defined views(urlHandler). """


from django.urls import path 
from . import views 

""" URL request and the urls that handles those request."""
urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add, name='add_video'),
    path('video_list', views.video_list, name='video_list')
]

