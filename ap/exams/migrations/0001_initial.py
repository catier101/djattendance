# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20160528_1628'),
        ('classes', '0002_class'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, blank=True)),
                ('is_open', models.BooleanField(default=False)),
                ('duration', models.DurationField(default=datetime.timedelta(0, 5400))),
                ('category', models.CharField(max_length=1, choices=[(b'M', b'Midterm'), (b'F', b'Final')])),
                ('total_score', models.DecimalField(default=0.0, max_digits=5, decimal_places=2)),
                ('training_class', models.ForeignKey(to='classes.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Responses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('responses', django.contrib.postgres.fields.hstore.HStoreField(null=True)),
                ('score', models.DecimalField(max_digits=5, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Retake',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_complete', models.BooleanField(default=False)),
                ('time_opened', models.DateTimeField(auto_now_add=True)),
                ('exam', models.ForeignKey(to='exams.Exam')),
                ('trainee', models.ForeignKey(to='accounts.Trainee')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instructions', models.TextField(null=True, blank=True)),
                ('section_index', models.IntegerField(default=0)),
                ('first_question_index', models.IntegerField(default=1)),
                ('question_count', models.IntegerField()),
                ('questions', django.contrib.postgres.fields.hstore.HStoreField(null=True)),
                ('exam', models.ForeignKey(related_name='sections', to='exams.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_submitted_online', models.BooleanField(default=True)),
                ('is_complete', models.BooleanField(default=False)),
                ('is_graded', models.BooleanField(default=False)),
                ('retake_number', models.IntegerField(default=0)),
                ('grade', models.DecimalField(default=0, max_digits=5, decimal_places=2)),
                ('exam', models.ForeignKey(to='exams.Exam')),
                ('trainee', models.ForeignKey(to='accounts.Trainee')),
            ],
        ),
        migrations.AddField(
            model_name='responses',
            name='section',
            field=models.ForeignKey(to='exams.Section'),
        ),
        migrations.AddField(
            model_name='responses',
            name='session',
            field=models.ForeignKey(to='exams.Session'),
        ),
    ]
