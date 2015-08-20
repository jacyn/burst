# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20150817_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='redirect_url',
            field=models.CharField(max_length=100, null=True, verbose_name='Redirect URL after submitting the survey form.', blank=True),
            preserve_default=True,
        ),
    ]
