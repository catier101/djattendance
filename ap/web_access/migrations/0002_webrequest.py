# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_statistics_trainee_trainingassistant_user'),
        ('web_access', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'P', max_length=2, choices=[(b'P', b'Pending'), (b'A', b'Approved'), (b'F', b'Marked for Fellowship'), (b'D', b'Denied'), (b'E', b'Expired')])),
                ('reason', models.CharField(max_length=2, choices=[(b'Go', b'Gospel'), (b'Sr', b'Service'), (b'GA', b'Graduate Application'), (b'Fs', b'Fellowship'), (b'Ot', b'Other')])),
                ('minutes', models.PositiveSmallIntegerField(choices=[(15, b'15 minutes'), (30, b'30 minutes'), (45, b'45 minutes'), (60, b'1 hour'), (90, b'1 hour 30 minutes'), (120, b'2 hours'), (180, b'3 hours'), (240, b'4 hours'), (300, b'5 hours')])),
                ('date_assigned', models.DateTimeField(auto_now_add=True)),
                ('time_started', models.DateTimeField(null=True, blank=True)),
                ('date_expire', models.DateField()),
                ('comments', models.TextField(null=True, blank=True)),
                ('TA_comments', models.TextField(null=True, blank=True)),
                ('trainee', models.ForeignKey(to='accounts.Trainee')),
            ],
            options={
                'ordering': ['date_assigned', 'date_expire', 'trainee__firstname'],
            },
        ),
    ]
