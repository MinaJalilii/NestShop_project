from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=11, unique=True, validators=[])

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def profile(self):
        profile = Profile.objects.get(user=self)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pictures')
    verified = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    post_save.connect(create_user_profile, sender=User)
    post_save.connect(save_user_profile, sender=User)

    def __str__(self):
        return self.full_name

    def user_image(self):
        return mark_safe('<img src="%s" width="50"  height="50" />' % self.image.url)


class ContactUs(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.full_name
