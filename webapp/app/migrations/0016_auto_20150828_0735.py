# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20150828_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='text_align',
            field=models.CharField(default=b'left', max_length=64, choices=[(b'left', b'Left'), (b'right', b'Right'), (b'center', b'Center')]),
            preserve_default=True,
        ),
    ]
