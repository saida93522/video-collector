"""video URL CORE URL Configuration for this project
 """

from django.contrib import admin
from django.urls import path, include 


""" links to the app's urls file, which then mapps to work with the defined urlHandler(views). """
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('video_collection.urls'))
]

