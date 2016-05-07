# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('absent_trainee_roster', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Absentee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=2, choices=[(b'C', b'Conference'), (b'SI', b'Sick'), (b'SE', b'Service'), (b'O', b'Other'), (b'T', b'Out of Town'), (b'F', b'Fatigue')])),
                ('coming_to_class', models.BooleanField(default=False)),
                ('comments', models.CharField(max_length=250, blank=True)),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
        ),
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('date', models.DateField(serialize=False, primary_key=True)),
            ],
        ),
    ]
