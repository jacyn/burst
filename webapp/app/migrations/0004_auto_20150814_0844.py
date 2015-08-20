# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150814_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='page',
            field=models.ForeignKey(related_name='objects', default=1, verbose_name='Page Object', to='app.Page'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='object',
            unique_together=set([('page', 'code')]),
        ),
    ]
