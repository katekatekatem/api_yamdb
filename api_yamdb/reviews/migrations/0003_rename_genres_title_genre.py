# Generated by Django 3.2 on 2023-05-19 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_comments_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='genres',
            new_name='genre',
        ),
    ]
