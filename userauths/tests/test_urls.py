from django.test import TestCase
from userauths.views import *
from django.urls import reverse, resolve


class TestUrls(TestCase):
    def test_sign_up(self):
        url = reverse('userauths:sign-up')
        self.assertEqual(resolve(url).func, sign_up_view)

    def test_sign_in(self):
        url = reverse('userauths:sign-in')
        self.assertEqual(resolve(url).func, sign_in_view)

    def test_sign_out(self):
        url = reverse('userauths:sign-out')
        self.assertEqual(resolve(url).func, sign_out_view)

    def test_contact_us(self):
        url = reverse('userauths:contact-us')
        self.assertEqual(resolve(url).func, contact_us)

    def test_contact_us_ajax(self):
        url = reverse('userauths:contact-us-ajax')
        self.assertEqual(resolve(url).func, ajax_contact_us)

    def test_edit_profile(self):
        url = reverse('userauths:edit-profile')
        self.assertEqual(resolve(url).func, edit_profile)

    def test_change_password(self):
        url = reverse('userauths:change-password')
        self.assertEqual(resolve(url).func, change_password)
