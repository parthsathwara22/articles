# Generated by Django 5.1.5 on 2025-03-02 20:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_alter_article_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publish',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
