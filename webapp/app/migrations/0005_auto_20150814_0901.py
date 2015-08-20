# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150814_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 9, 1, 0, 743482), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='object',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 9, 1, 12, 551437), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 9, 1, 18, 695280), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 9, 1, 24, 279490), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='surveyquestion',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 9, 1, 30, 271307), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='surveyquestion',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 9, 1, 33, 471451), auto_now=True),
            preserve_default=False,
        ),
    ]
