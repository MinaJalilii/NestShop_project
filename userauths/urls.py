from django.urls import path
from userauths.views import *

app_name = 'userauths'
urlpatterns = [
    path('user/sign-up', sign_up_view, name='sign-up'),
    path('user/sign-in', sign_in_view, name='sign-in'),
    path('user/sign-out', sign_out_view, name='sign-out'),
    path('user/contact-us', contact_us, name="contact-us"),
    path('contact-us-ajax', ajax_contact_us, name="contact-us-ajax"),
    path('edit-profile', edit_profile, name="edit-profile"),
    path('change-password', change_password, name='change-password'),
]
