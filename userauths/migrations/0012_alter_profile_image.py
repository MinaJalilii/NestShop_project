# Generated by Django 5.0.2 on 2024-05-08 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0011_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='profile_pictures'),
        ),
    ]