# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20150826_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='background_transparency',
            field=models.IntegerField(default=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='font_color',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='font_size',
            field=models.IntegerField(default=12, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='text_align',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
    ]
