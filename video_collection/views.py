from django.shortcuts import render, redirect,get_object_or_404
from .models import Video
from .forms import VideoForm, SearchForm
from django.contrib import messages 
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower
from django.http import HttpResponseForbidden,HttpResponse


def home(request):
    app_name = 'Travel Videos'
    return render(request, 'video_collection/home.html', {'app_name': app_name})

def add(request):
    """ add and verify videos using form model objects and save to database. """
    if request.method == 'POST':   # adding a new video
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            try:
                new_video_form.save()  # Creates new Video object and saves 
                return redirect('video_list')
            except IntegrityError:
                messages.warning(request, 'You already added that video')
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
        
        # Invalid form 
        messages.warning(request, 'Check the data entered')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form}) 
            
    new_video_form = VideoForm()
    context = {'new_video_form':new_video_form}
    return render(request, 'video_collection/add.html', context) 



def delete(request,video_pk):
    """ delete the video data of the current user(pk). 
        :param: request object for a place that was visited."""
    video = Video.objects.get(pk=video_pk) 
    # get_object_or_404(Video, pk=video_pk)
    
    if request.method == 'POST':
        video.delete()
        return redirect('video_list')
    else:
        return HttpResponseForbidden()


def video_details(request,video_pk):
    # if request.method
    video = get_object_or_404(Video, pk=video_pk)
    # page_err = HttpResponse.status_code(404)
    if HttpResponse.status_code == 404:
        messages.error(request,'page not found')
    return render(request,'video_collection/video_details.html',{'video':video})
    #  HttpResponseNotFound:
    #     messages.error('Video does not exist')
    
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

