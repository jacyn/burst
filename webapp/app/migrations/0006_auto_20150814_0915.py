# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20150814_0901'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='object',
            unique_together=set([]),
        ),
    ]
