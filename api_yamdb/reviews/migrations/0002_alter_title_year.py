# Generated by Django 3.2 on 2023-05-10 21:17

from django.db import migrations, models
import reviews.models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(default=0, validators=[reviews.models.validate_yaer]),
        ),
    ]