# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20150828_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='background_transparency',
            field=models.IntegerField(default=100, null=True, blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
            preserve_default=True,
        ),
    ]
