# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20150814_0915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='page',
        ),
    ]
