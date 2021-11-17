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
    if request.method == 'POST':  
        new_video_form = VideoForm(request.POST) #form now equals the data requested with
        if new_video_form.is_valid(): #verify that the data matches
            try:
                new_video_form.save()  # Creates new Video object and saves 
                return redirect('video_list')
            except IntegrityError:
                messages.warning(request, 'You already added that video')
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
        
        # Invalid form 
        messages.warning(request, 'Check the data entered')
        context = {'new_video_form': new_video_form}
        return render(request, 'video_collection/add.html',context) 
            
        
    new_video_form = VideoForm()
    context = {'new_video_form':new_video_form}
    return render(request, 'video_collection/add.html', context) 
    



