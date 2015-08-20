# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_object_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='survey',
        ),
        migrations.AddField(
            model_name='survey',
            name='page_object',
            field=models.ForeignKey(related_name='survey', blank=True, to='app.Object', null=True),
            preserve_default=True,
        ),
    ]
