# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_statistics_trainee_trainingassistant_user'),
        ('schedules', '0002_auto_20160504_1806'),
        ('leaveslips', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupSlip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=5, choices=[(b'CONF', b'Conference'), (b'EMERG', b'Family Emergency'), (b'FWSHP', b'Fellowship'), (b'FUNRL', b'Funeral'), (b'GOSP', b'Gospel'), (b'INTVW', b'Grad School/Job Interview'), (b'GRAD', b'Graduation'), (b'MEAL', b'Meal Out'), (b'NIGHT', b'Night Out'), (b'OTHER', b'Other'), (b'SERV', b'Service'), (b'SICK', b'Sickness'), (b'SPECL', b'Special'), (b'WED', b'Wedding'), (b'NOTIF', b'Notification Only')])),
                ('status', models.CharField(default=b'P', max_length=1, choices=[(b'A', b'Approved'), (b'P', b'Pending'), (b'F', b'Fellowship'), (b'D', b'Denied'), (b'S', b'TA sister approved')])),
                ('submitted', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('finalized', models.DateTimeField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('texted', models.BooleanField(default=False)),
                ('informed', models.BooleanField(default=False)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('TA', models.ForeignKey(to='accounts.TrainingAssistant')),
                ('trainee', models.ForeignKey(to='accounts.Trainee')),
                ('trainees', models.ManyToManyField(related_name='group', to='accounts.Trainee')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IndividualSlip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=5, choices=[(b'CONF', b'Conference'), (b'EMERG', b'Family Emergency'), (b'FWSHP', b'Fellowship'), (b'FUNRL', b'Funeral'), (b'GOSP', b'Gospel'), (b'INTVW', b'Grad School/Job Interview'), (b'GRAD', b'Graduation'), (b'MEAL', b'Meal Out'), (b'NIGHT', b'Night Out'), (b'OTHER', b'Other'), (b'SERV', b'Service'), (b'SICK', b'Sickness'), (b'SPECL', b'Special'), (b'WED', b'Wedding'), (b'NOTIF', b'Notification Only')])),
                ('status', models.CharField(default=b'P', max_length=1, choices=[(b'A', b'Approved'), (b'P', b'Pending'), (b'F', b'Fellowship'), (b'D', b'Denied'), (b'S', b'TA sister approved')])),
                ('submitted', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('finalized', models.DateTimeField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('texted', models.BooleanField(default=False)),
                ('informed', models.BooleanField(default=False)),
                ('TA', models.ForeignKey(to='accounts.TrainingAssistant')),
                ('events', models.ManyToManyField(related_name='leaveslip', to='schedules.Event')),
                ('trainee', models.ForeignKey(to='accounts.Trainee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
