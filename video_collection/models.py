from urllib import parse 
from django.db import models
from django.core.exceptions import ValidationError

class Video(models.Model):
    """ video model fields maps to video table in db. """
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True)
    objects = models.Manager()

   
                    
    def __str__(self):
        # String displayed in the admin console, or when printing a model object. 
        # You can return any useful string here. Optionally 
        if not self.notes:
            notes = 'No notes'
        else:
            notes = self.notes[1:200]
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url},  \
        Video ID:,  Notes: {notes}'
