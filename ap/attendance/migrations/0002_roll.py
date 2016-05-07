# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_statistics_trainee_trainingassistant_user'),
        ('schedules', '0002_auto_20160504_1806'),
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'P', max_length=5, choices=[(b'A', b'Absent'), (b'T', b'Tardy'), (b'U', b'Uniform'), (b'L', b'Left Class'), (b'P', b'Present')])),
                ('finalized', models.BooleanField(default=False)),
                ('notes', models.CharField(max_length=200, blank=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(to='schedules.Event')),
                ('monitor', models.ForeignKey(related_name='submitted_rolls', to='accounts.Trainee', null=True)),
                ('trainee', models.ForeignKey(related_name='rolls', to='accounts.Trainee')),
            ],
        ),
    ]
