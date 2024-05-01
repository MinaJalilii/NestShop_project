from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from userauths.views import *
from userauths.models import *
from django.contrib.messages import get_messages
from model_bakery import baker


class TestSignUpView(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('userauths:sign-up')

    def test_get_request_unauthenticated_user(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userauths/sign_up.html')
        self.failUnless(response.context['form'], SignUpForm)

    def test_get_request_authenticated_user(self):
        user = User.objects.create_user(username='testy', email='testy@email.com', password='testy-password')
        self.client.force_login(user)
        response = self.client.get(self.signup_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, reverse('home:home'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You're already Logged In.")
        self.assertEqual(messages[0].level, 30)

    def test_POST_valid_data(self):
        data = {
            'username': 'test-user',
            'email': 'test-user@email.com',
            'phone': '05419322587',
            'password1': 'test-password',
            'password2': 'test-password',
        }
        response = self.client.post(self.signup_url, data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))
        self.assertTrue(User.objects.filter(username='test-user').exists())
        self.assertTrue(authenticate(username='test-user@email.com', password='test-password'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, 25)
        self.assertEqual(str(messages[0]), "Hello test-user, your account created successfully.")

    def test_POST_invalid_data(self):
        data = {
            'username': 'test-user1',
            'email': 'InvalidEmail',
            'phone': '05419432587',
            'password1': 'test-password1',
            'password2': 'test-password1',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response.context['form'], 'email', 'Enter a valid email address.')

    def test_POST_password_mismatch(self):
        data = {
            'username': 'test-user2',
            'email': 'testuser2@email.com',
            'phone': '09254569852',
            'password1': 'test-password2',
            'password2': 'test-password1',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'password2', 'The two password fields didn’t match.')


class TestSignInView(TestCase):

    def setUp(self):
        self.client = Client()
        self.signin_url = reverse('userauths:sign-in')
        self.user = User.objects.create_user(username='mina', email='mina@email.com', password='mina-password')

    def test_get_request_unauthenticated_user(self):
        response = self.client.get(self.signin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userauths/sign_in.html')

    def test_get_request_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.signin_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, reverse('home:home'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You're already Logged In.")
        self.assertEqual(messages[0].level, 30)

    def test_POST_valid_data(self):
        data = {
            'email': 'mina@email.com',
            'password': 'mina-password',
        }
        response = self.client.post(self.signin_url, data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You're logged in successfully.")
        self.assertEqual(messages[0].level, 25)
        self.assertEqual(response.status_code, 302)

    def test_POST_invalid_data(self):
        data = {
            'email': 'invalid@email.com',
            'password': 'invalid-password',
        }
        response = self.client.post(self.signin_url, data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "User doesn't exist, create account.")
        self.assertEqual(messages[0].level, 30)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userauths/sign_in.html')


class TestSignOutView(TestCase):
    def setUp(self):
        self.client = Client()
        self.sign_out_url = reverse('userauths:sign-out')
        self.user = User.objects.create_user(username='test-user', email='test-user@email.com',
                                             password='test-user-password')

    def test_GET_request(self):
        self.client.force_login(self.user)
        response = self.client.get(self.sign_out_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You're logged out successfully.")
        self.assertEqual(messages[0].level, 25)

    def test_POST_request(self):
        response = self.client.post(self.sign_out_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You're logged out successfully.")
        self.assertEqual(messages[0].level, 25)


class TestContactUsView(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact_url = reverse('userauths:contact-us')

    def test_GET_request(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userauths/contact_us.html')


class TestAjaxContactUsView(TestCase):

    def setUp(self):
        self.client = Client()
        self.contact_url = reverse("userauths:contact-us-ajax")

    def test_GET_request_valid(self):
        data = {
            'full_name': 'test fullname',
            'email': 'test@email.com',
            'phone': '09456378264',
            'subject': 'test subject',
            'message': 'test message',
        }

        response = self.client.get(self.contact_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        contact_us_object = ContactUs.objects.first()
        self.assertIsNotNone(contact_us_object)
        self.assertEqual(contact_us_object.full_name, 'test fullname')
        self.assertEqual(contact_us_object.email, 'test@email.com')
        self.assertEqual(contact_us_object.phone, '09456378264')
        self.assertEqual(contact_us_object.subject, 'test subject')
        self.assertEqual(contact_us_object.message, 'test message')
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {'boolean': True})


class TestEditProfileView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('userauths:edit-profile')
        self.user = User.objects.create_user(username='mina', email='mina@email.com', password='mina-password')
        self.client.force_login(self.user)

    def test_authenticated_existing_profile(self):
        baker.make(Profile, user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userauths/edit-profile.html')

    def test_authenticated_not_existing_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userauths/edit-profile.html')
        self.assertIn('form', response.context)
        self.assertIn('profile', response.context)
        self.assertIsNone(response.context['profile'])
        self.assertIsInstance(response.context['form'], EditProfileForm)

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_POST_valid_data(self):
        baker.make(Profile, user=self.user)
        image = SimpleUploadedFile(name='author-2.png',
                                   content=open('media/profile_pictures/author-2.png', 'rb').read(),
                                   content_type='image/png')
        data = {
            'full_name': 'John Doe',
            'display_name': 'John',
            'bio': 'Test bio',
            'image': image
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('home:dashboard'))
        self.assertEqual(response.status_code, 302)
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(len(message), 1)
        self.assertEqual(str(message[0]), 'Profile updated successfully.')
        self.assertEqual(message[0].level, 25)

    def test_POST_invalid_data(self):
        baker.make(Profile, user=self.user)
        data = {
            'full_name': 'John Doe',
            'display_name': 'John',
            'bio': 'Test bio',
            'image': 'invalid image'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'image', 'This field is required.')


class TestChangePasswordView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('userauths:change-password')
        self.user = User.objects.create_user(username='bita', email='bita@email.com', password='bita-password')
        self.client.force_login(self.user)

    def test_authenticated_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userauths/change-password.html')
        self.assertIn('form1', response.context)
        self.assertIsInstance(response.context['form1'], ChangePasswordForm)

    def test_not_authenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_POST_valid_data(self):
        data = {
            'current_password': 'bita-password',
            'password1': 'changed-password',
            'password2': 'changed-password',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('userauths:sign-in'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_POST_invalid_data(self):
        data = {
            'current_password': 'bita-password',
            'password1': 'changed-password',
            'password2': 'changed-passwordd',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form1'], 'password2', "Passwords are not the same..")
