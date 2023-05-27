# Generated by Django 3.2 on 2023-05-21 19:46

import reviews.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(validators=[reviews.validators.validate_title_year]),
        ),
    ]