# Generated by Django 4.2.5 on 2023-10-23 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_productreview_product_alter_productreview_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='parent',
        ),
    ]
