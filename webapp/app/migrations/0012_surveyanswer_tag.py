# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20150817_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyanswer',
            name='tag',
            field=models.CharField(default='1_123456_20150818113800', max_length=64, verbose_name='Tag'),
            preserve_default=False,
        ),
    ]
