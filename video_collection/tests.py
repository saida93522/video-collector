from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from .models import Video

class TestHomePageMessage(TestCase):
    def test_app_title_message_shown_on_home_page(self):
        """ test the home page shows the title."""
        # make req to homepage using url name
        url = reverse('home')

        # object client
        response = self.client.get(url)
        self.assertContains(response, 'Travel Videos')

class TestAddVideos(TestCase):
    """ test video added is valid."""
    def test_add_video(self):
        # Arrange
        valid_video = {
            'name': 'Visit Hawaii',
            'url':'https://www.youtube.com/watch?v=0XoT1z-gAQw',
            'notes': '10 places to visit in Hawaii.'
        }
        # Act
        url = reverse('add_video')
        response = self.client.post(url,data=valid_video, follow=True) #if request redirects,follow
        
        #assert video list shows new video
        self.assertTemplateUsed('video_collection/video_list.html')
        self.assertContains(response,'Visit Hawaii')
        self.assertContains(response,'https://www.youtube.com/watch?v=0XoT1z-gAQw')
        self.assertContains(response,'10 places to visit in Hawaii.')

        #assert number of videos returned is correct
        video_count = Video.objects.count() # sql_syntax ---> SELECT COUNT(*) 
        self.assertEqual(1,video_count)

        video = Video.objects.first() # returns the first video object or None
        self.assertEqual('Visit Hawaii',video.name)
        self.assertEqual('https://www.youtube.com/watch?v=0XoT1z-gAQw',video.url)
        self.assertEqual('10 places to visit in Hawaii.',video.notes)
        self.assertEqual('0XoT1z-gAQw', video.video_id)

    def test_add_video_invalid_url_not_added(self):
        #Arrange
        invalid_video_urls = [
            'https://www.youtube.com',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?abc=123',
            'https://minneapolis.learn.minnstate.edu/d2l/',
            'https://minneapolis.edu?v=344553',
            'https://github.com'
        ]
        #Act
        for invalid_urls in invalid_video_urls:
            new_video = {
                'name':'example',
                'url':invalid_urls,
                'notes':'example note'
            }
            url = reverse('add_video')
            response = self.client.post(url,new_video)

        msg_dict = response.context['messages']
        msg_text = [message.message for message in msg_dict]

        #assert error message is returned for every invalid video
        self.assertTemplateUsed('video_collection/add.html')
        self.assertIn('Invalid YouTube URL',msg_text)
        self.assertIn('Check the data entered',msg_text)

        # check there is no data in the database
        video_count = Video.objects.count()
        self.assertEqual(0, video_count)
        
class TestVideoList(TestCase):
    """ test the 'video list' request displays the list of videos user added."""
    pass            

class TestVideoSearch(TestCase):
    """ test"""
    pass

class TestVideoModel(TestCase):
    """ test"""
    pass
    
    