# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import filer.fields.image
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(default=b'', max_length=255)),
                ('sequence', models.IntegerField(default=0)),
                ('name', models.CharField(default=b'', max_length=255)),
                ('x', models.DecimalField(max_digits=30, decimal_places=25)),
                ('y', models.DecimalField(max_digits=30, decimal_places=25)),
                ('width', models.DecimalField(max_digits=30, decimal_places=25)),
                ('height', models.DecimalField(max_digits=30, decimal_places=25)),
                ('background_width', models.DecimalField(null=True, max_digits=30, decimal_places=25, blank=True)),
                ('background_height', models.DecimalField(null=True, max_digits=30, decimal_places=25, blank=True)),
                ('background_color', models.CharField(max_length=255, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('background_image', filer.fields.image.FilerImageField(related_name='background_images', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='filer.Image', null=True)),
            ],
            options={
                'verbose_name': 'Object',
                'verbose_name_plural': 'Objects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(default=b'', max_length=64, verbose_name='Slug')),
                ('name', models.CharField(default=b'', help_text='Name of the Page.', max_length=128, verbose_name='Name')),
                ('datetime_added', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(related_name='pages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(default=b'', unique=True, max_length=64, verbose_name='Slug')),
                ('name', models.CharField(default=b'', help_text='Name of the Project.', max_length=128, verbose_name='Name')),
                ('description', models.CharField(max_length=512, null=True, verbose_name='Description', blank=True)),
                ('datetime_added', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(related_name='projects', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(related_name='projects', verbose_name='Project Owner', to='accounting.Client')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Title for the Survey Form.', max_length=100, null=True, verbose_name='Title', blank=True)),
                ('slug', models.SlugField(default=b'', unique=True, max_length=100, verbose_name='Slug')),
                ('thanks', models.TextField(verbose_name='Message displayed after submitting the survey form.')),
                ('submit', models.CharField(max_length=30, verbose_name='Text for the Submit button.', blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Survey',
                'verbose_name_plural': 'Surveys',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=1000, null=True, verbose_name='Answer', blank=True)),
                ('test_mode', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Survey Answer',
                'verbose_name_plural': 'Survey Answers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100, verbose_name='Question')),
                ('slug', models.SlugField(default=b'', max_length=100, blank=True, unique=True, verbose_name='Slug')),
                ('field_type', models.IntegerField(max_length=100, verbose_name='Answer Type', choices=[(1, 'Single line text'), (2, 'Multi line text'), (3, 'Email'), (13, 'Number'), (14, 'URL'), (4, 'Check box'), (5, 'Check boxes'), (6, 'Drop down'), (7, 'Multi select'), (8, 'Radio buttons'), (9, 'File upload'), (10, 'Date'), (11, 'Date/time'), (15, 'Date of birth'), (12, 'Hidden')])),
                ('initial', models.CharField(max_length=250, null=True, verbose_name='Inital Value', blank=True)),
                ('placeholder_text', models.CharField(max_length=100, null=True, verbose_name='Placeholder Text', blank=True)),
                ('choices', models.CharField(help_text=b'Comma separated options where applicable. If an option itself contains commas, surround the option starting with the `character and ending with the ` character.', max_length=1000, verbose_name='Choices', blank=True)),
                ('required', models.BooleanField(default=True, verbose_name='Required Field')),
                ('default', models.CharField(max_length=2000, verbose_name='Default value', blank=True)),
                ('help_text', models.CharField(max_length=100, verbose_name='Help text', blank=True)),
                ('active', models.BooleanField(default=True)),
                ('survey', models.ForeignKey(related_name='survey_questions', verbose_name='Survey Form', to='app.Survey')),
            ],
            options={
                'verbose_name': 'Survey Question',
                'verbose_name_plural': 'Survey Questions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='question',
            field=models.ForeignKey(related_name='survey_answers', verbose_name='Survey Question', to='app.SurveyQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='survey',
            field=models.ForeignKey(related_name='survey_answers', verbose_name='Survey Form', to='app.Survey'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='project',
            field=models.ForeignKey(related_name='project_pages', default=b'', verbose_name='Project Page', to='app.Project'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('project', 'slug')]),
        ),
        migrations.AddField(
            model_name='object',
            name='survey',
            field=models.ForeignKey(related_name='project_objects', blank=True, to='app.Survey', null=True),
            preserve_default=True,
        ),
    ]
