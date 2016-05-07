# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0002_class'),
        ('terms', '0002_term'),
        ('accounts', '0002_statistics_trainee_trainingassistant_user'),
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('code', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=250, blank=True)),
                ('type', models.CharField(max_length=1, choices=[(b'C', b'Class'), (b'S', b'Study'), (b'M', b'Meal'), (b'H', b'House'), (b'T', b'Team'), (b'L', b'Church Meeting'), (b'*', b'Special')])),
                ('monitor', models.CharField(blank=True, max_length=2, null=True, choices=[(b'AM', b'Attendance Monitor'), (b'TM', b'Team Monitor'), (b'HC', b'House Coordinator')])),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('classs', models.ForeignKey(verbose_name=b'class', blank=True, to='classes.Class', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('code', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=250, blank=True)),
                ('repeat', models.CommaSeparatedIntegerField(max_length=20)),
                ('duration', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('events', models.ManyToManyField(to='schedules.Event', blank=True)),
                ('term', models.ForeignKey(to='terms.Term')),
                ('trainee', models.ForeignKey(related_name='schedule', to='accounts.Trainee')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('eventgroup', models.ManyToManyField(to='schedules.EventGroup')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='group',
            field=models.ForeignKey(related_name='events', blank=True, to='schedules.EventGroup', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='term',
            field=models.ForeignKey(to='terms.Term'),
        ),
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together=set([('trainee', 'term')]),
        ),
    ]
