from django.test import TestCase
from userauths.models import *
from model_bakery import baker


class TestModels(TestCase):
    def test_profile_model_str(self):
        profile = baker.make(Profile, full_name='mina jalili')
        self.assertEqual(str(profile), 'mina jalili')

    def test_user_image(self):
        image_url = '/media/profile_pictures/author-2.png'
        profile = Profile(image=image_url)
        image_html = profile.user_image()
        self.assertIn(image_url, image_html)
        self.assertIn('width="50"', image_html)
        self.assertIn('height="50"', image_html)

    def test_contact_us_model_str(self):
        contact_us = baker.make(ContactUs, full_name='mina jalili')
        self.assertEqual(str(contact_us), 'mina jalili')
