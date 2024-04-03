# Generated by Django 5.0.2 on 2024-04-02 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_productreview_review_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='core.productreview'),
        ),
    ]