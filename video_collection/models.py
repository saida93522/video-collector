from urllib import parse 
from django.db import models
from django.core.exceptions import ValidationError

class Video(models.Model):
    """ video model fields maps to video table in db. """
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=40, unique=True) # https://www.youtube.com/watch?v=video_id
    objects = models.Manager()

    
    def save(self, *args, **kwargs):
        """ overrides save method and verrifies youtube url is valid before saved to db.Extracts the video id from the URL if valid."""
        try:
            url_components = parse.urlparse(self.url)

            if url_components.scheme != 'https':
                raise ValidationError(f'Not a YouTube URL {self.url}')
            # netloc--where the request is made to.
            if url_components.netloc != 'www.youtube.com':
                raise ValidationError(f'Not a YouTube URL {self.url}')
                
            if url_components.path != '/watch':
                raise ValidationError(f'Not a YouTube URL {self.url}')
            
            query_string = url_components.query
            if not query_string:
                raise ValidationError(f'Invalid YouTube URL {self.url}')
            parameters = parse.parse_qs(query_string, strict_parsing=True) #converts video_id to dict = {'v_id':45344}
            v_parameter_list = parameters.get('v')
            if not v_parameter_list:   # rais error if v=non or an empty list
                raise ValidationError(f'Invalid YouTube URL parameters {self.url}')
            self.video_id = v_parameter_list[0]   # set the video_id
        except ValueError as e:  
            raise ValidationError(f'Unable to parse URL {self.url}') from e

        super().save(*args, **kwargs)  

   
                    
    def __str__(self):
        # String displayed in the admin console, or when printing a model object. 
        # You can return any useful string here. Optionally 
        if not self.notes:
            notes = 'No notes'
        else:
            notes = self.notes[1:200]
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url},  \
        Video ID{self.video_id}:,  Notes: {notes}'
