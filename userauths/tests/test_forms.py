from userauths.forms import *
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.test import TestCase
from PIL import Image
from io import BytesIO


class TestSignUpForm(TestCase):
    def test_valid_data(self):
        form = SignUpForm(data={
            'username': 'mina',
            'email': 'mina@email.com',
            'phone': '09123456789',
            'password1': '00006987Mina',
            'password2': '00006987Mina',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)


class TestChangePasswordForm(TestCase):
    def test_valid_data(self):
        form = ChangePasswordForm(data={
            'current_password': '00006987Mina',
            'password1': '00001234Mina',
            'password2': '00001234Mina',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = ChangePasswordForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_passwords_are_not_match(self):
        form = ChangePasswordForm(data={
            'current_password': '00006987Mina',
            'password1': '00001234Mina',
            'password2': '000012345Mina',
        })
        self.assertTrue(form.has_error)
        self.assertEqual(len(form.errors), 1)
