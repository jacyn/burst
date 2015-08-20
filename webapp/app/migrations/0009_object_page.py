# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20150814_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='page',
            field=models.ForeignKey(related_name='objects', default=1, verbose_name='Page', to='app.Page'),
            preserve_default=False,
        ),
    ]
