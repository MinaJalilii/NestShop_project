# Generated by Django 5.0.2 on 2024-04-03 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0009_profile_is_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='/assets/imgs/profile/defult.jpg', upload_to='profile_pictures'),
        ),
    ]