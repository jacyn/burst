# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150814_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='project',
            field=models.ForeignKey(related_name='pages', verbose_name='Project Page', to='app.Project'),
            preserve_default=True,
        ),
    ]
