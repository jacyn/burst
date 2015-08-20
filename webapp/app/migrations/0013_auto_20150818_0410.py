# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_surveyanswer_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_mode', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('survey', models.ForeignKey(related_name='results', verbose_name='Survey Form', to='app.Survey')),
            ],
            options={
                'verbose_name': 'Survey Result',
                'verbose_name_plural': 'Survey Results',
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='surveyanswer',
            old_name='answer',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='surveyanswer',
            name='survey',
        ),
        migrations.RemoveField(
            model_name='surveyanswer',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='surveyanswer',
            name='test_mode',
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='result',
            field=models.ForeignKey(related_name='answers', default=1, verbose_name='Survey Result', to='app.SurveyResult'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='surveyanswer',
            name='question',
            field=models.ForeignKey(related_name='answers', verbose_name='Survey Question', to='app.SurveyQuestion'),
            preserve_default=True,
        ),
    ]
