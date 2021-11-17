from django.shortcuts import render, redirect
from .models import Video
from .forms import VideoForm, SearchForm
from django.contrib import messages 
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower


def home(request):
    app_name = 'Travel Videos'
    return render(request, 'video_collection/home.html', {'app_name': app_name})


def add(request):
    """ add and verify videos using form model objects and save to database. """
    return render(request, 'video_collection/add.html', context) 

