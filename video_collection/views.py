from django.shortcuts import render, redirect,get_object_or_404
from .models import Video
from .forms import VideoForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower
from django.http import HttpResponseForbidden


@login_required
def home(request):
    app_name = 'Travel Videos'
    return render(request, 'video_collection/home.html', {'app_name': app_name})

@login_required
def add(request):
    """ add and verify videos using form model objects and save to database. """
    new_video_form = VideoForm()
    if request.method == 'POST':  
        new_video_form = VideoForm(request.POST) #form now equals the data requested with
        video = new_video_form.save(commit=False)
        video.user =request.user
        if new_video_form.is_valid(): #verify that the data matches
            try:
                new_video_form.save()
                return redirect('video_list')
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
            except IntegrityError:
                messages.warning(request, 'You already added that video')
        
        #Invalid form 
        messages.warning(request, 'Check the data entered')
        context = {'new_video_form': new_video_form}
        return render(request, 'video_collection/add.html',context) 
            
        
    new_video_form = VideoForm()
    context = {'new_video_form':new_video_form}
    return render(request, 'video_collection/add.html', context) 

@login_required
def delete(request,video_pk):
    """ delete the video data of the current user(pk). 
        :param: request object for a place that was visited."""
        
    video = get_object_or_404(Video, pk=video_pk)
    if video.user == request.user:
        video.delete()
        return redirect('video_list')
    else:
        return HttpResponseForbidden()


@login_required
def video_details(request,video_pk):
    video = get_object_or_404(Video, pk=video_pk)
    if video.user != request.user:
        return HttpResponseForbidden()
    else:
        return render(request,'video_collection/video_details.html',{'video':video})
 
    
@login_required
def video_list(request):
    """ displays the list of videos user saved/added
    returns:list of videos template or the data user searched for.
    """

    search_form = SearchForm(request.GET) #form now equals the data user requested with

    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name'))

    else:
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name'))

    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form})

