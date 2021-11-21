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
        # self.assertContains(response,'https://www.youtube.com/watch?v=0XoT1z-gAQw')
        # self.assertContains(response,'10 places to visit in Hawaii.')

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
    """ test the 'video list' request displays the list of video/videos the user added."""
    def test_all_videos_display_in_the_correct_order(self):
        #Arrange
        v1 = Video.objects.create(name='abc',url='https://www.youtube.com/watch?v=0XoT1z-gAQw',notes='example notes1')
        v2 = Video.objects.create(name='FF4',url='https://www.youtube.com/watch?v=Wt4XODPm4hA',notes='example notes2')
        v3 = Video.objects.create(name='AAA',url='https://www.youtube.com/watch?v=TJERhGzxRK8',notes='example notes3')
        v4 = Video.objects.create(name='LMN',url='https://www.youtube.com/watch?v=bAEprBbAfZM',notes='example notes4')

        #Act
        expected_video_order = [v3,v1,v2,v4]
        url = reverse('video_list')
        response = self.client.get(url)
        videos_in_template = list(response.context['videos'])

        #Assert
        self.assertEqual(videos_in_template, expected_video_order)

    def test_no_video_message(self):
        url = reverse('video_list')
        response = self.client.get(url)
        self.assertContains(response, 'No videos.')
        self.assertEqual(0,len(response.context['videos']))        

    def test_video_number_message_one_video(self):
        Video.objects.create(name='LMN',url='https://www.youtube.com/watch?v=bAEprBbAfZM',notes='example notes1')
        url = reverse('video_list')
        response = self.client.get(url)
        
        self.assertContains(response, '1 video')
        self.assertNotContains(response, '1 videos')

    def test_video_number_message_more_than_one_video(self):
        #Arrange
        Video.objects.create(name='zzz',url='https://www.youtube.com/watch?v=abc123',notes='example notes1')
        Video.objects.create(name='dlr',url='https://www.youtube.com/watch?v=cba321',notes='example notes2')
        #Act
        url = reverse('video_list')
        response = self.client.get(url)

        #Assert
        self.assertContains(response, '2 videos')
    
class TestVideoSearch(TestCase):
    """ test the video search shows the matching videos or returns no videos """
    def test_video_search_that_match(self):
        #Arrange
        v1 = Video.objects.create(name='ABC',url='https://www.youtube.com/watch?v=0XoT1z-gAQw',notes='example notes1')
        v2 = Video.objects.create(name='abc',url='https://www.youtube.com/watch?v=fq70UHD8DrM',notes='example notes2')
        v3 = Video.objects.create(name='zlw',url='https://www.youtube.com/watch?v=uXyy7lgDj9k',notes='example notes3')
        v4 = Video.objects.create(name='visit',url='https://www.youtube.com/watch?v=NUDBwBJeKvY',notes='example notes4')

        #Action
        expected_search_order = [v1,v2]
        response = self.client.get(reverse('video_list') + '?search_term=abc')

        videos_in_order = list(response.context['videos'])

        #Assert
        self.assertEqual(expected_search_order,videos_in_order)

    def test_video_search_that_does_not_match(self):
        #Arrange
        Video.objects.create(name='ABC',url='https://www.youtube.com/watch?v=0XoT1z-gAQw',notes='example notes1')
        Video.objects.create(name='abc',url='https://www.youtube.com/watch?v=fq70UHD8DrM',notes='example notes2')
        Video.objects.create(name='zlw',url='https://www.youtube.com/watch?v=uXyy7lgDj9k',notes='example notes3')
        Video.objects.create(name='visit',url='https://www.youtube.com/watch?v=NUDBwBJeKvY',notes='example notes4')

        #Action
        expected_search_order = []
        response = self.client.get(reverse('video_list') + '?search_term=goldfish')

        videos_in_order = list(response.context['videos'])

        #Assert
        self.assertEqual(expected_search_order,videos_in_order)
        self.assertContains(response, 'No videos')
        

class TestVideoModel(TestCase):
    """ test video model query"""
    def test_invalid_url_raises_validation_error(self):
        #Arrange
        invalid_video_urls = [
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch/abc535',
            'https://www.youtube.com/watch?abc=123',
            'https://www.youtube.com/watch/fgwt44?v=1s323',
            'http://youtube.com/watch?v=Xffjeg7',
            'https://minneapolis.learn.minnstate.edu/d2l/',
            'https://minneapolis.edu?v=344553',
            'https://github.com'
        ]
        #Action/Assert
        for invalid_url in invalid_video_urls:
            with self.assertRaises(ValidationError):
                Video.objects.create(name='ABC',url=invalid_url,notes='example notes')
            #     new_video = {
            #     'name':'example',
            #     'url':invalid_urls,
            #     'notes':'example note'
            # }
                
        video_count = Video.objects.count()
        self.assertEqual(0, video_count)
    
    def test_duplicate_video_raises_integrity_error(self):
        #Arrange/Action
        Video.objects.create(name='ABC',url='https://www.youtube.com/watch?v=0XoT1z-gAQw',notes='example notes1')
        # Asser
        with self.assertRaises(IntegrityError):
            Video.objects.create(name='ABC',url='https://www.youtube.com/watch?v=0XoT1z-gAQw',notes='example notes1')

# class TestDeleteVideo(TestCase):
#     pass

class TestDetailVideo(TestCase):
    def test_a_detail_page_is_returned(self):
        Video.objects.create(name='LMN',url='https://www.youtube.com/watch?v=bAEprBbAfZM',notes='example notes1')
        url = reverse('video_details')
        # response = self.client.get(url)
    