from django import forms 
from .models import Video 


""" description of the form shown on the webpage. """
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video 
        fields = ['name', 'url', 'notes']


class SearchForm(forms.Form):
    """ search form field. """
    search_term = forms.CharField()



