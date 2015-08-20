# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_object_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='slug',
        ),
        migrations.AddField(
            model_name='survey',
            name='redirect_url',
            field=models.TextField(default=None, verbose_name='Redirect URL after submitting the survey form.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='object',
            name='page',
            field=models.ForeignKey(related_name='page_objects', verbose_name='Page', to='app.Page'),
            preserve_default=True,
        ),
    ]
