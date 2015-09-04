# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20150828_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyquestion',
            name='field_type',
            field=models.IntegerField(max_length=100, verbose_name='Answer Type', choices=[(1, 'Single line text'), (2, 'Multi line text'), (3, 'Email'), (16, b'Mobile Number'), (13, 'Number'), (4, 'Check box'), (5, 'Check boxes'), (6, 'Drop down'), (7, 'Multi select'), (8, 'Radio buttons'), (10, 'Date'), (11, 'Date/time'), (15, 'Date of birth')]),
            preserve_default=True,
        ),
    ]
