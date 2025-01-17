# Generated by Django 2.2.4 on 2019-09-03 19:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hasker', '0002_auto_20190902_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='down_votes',
            field=models.ManyToManyField(blank=True, related_name='answer_down', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='up_votes',
            field=models.ManyToManyField(blank=True, related_name='answer_up', to=settings.AUTH_USER_MODEL),
        ),
    ]
