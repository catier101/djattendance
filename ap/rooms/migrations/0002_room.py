# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('code', models.CharField(max_length=6, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('floor', models.SmallIntegerField()),
                ('type', models.CharField(blank=True, max_length=2, choices=[(b'Cr', b'Classroom'), (b'FR', b'Fellowship Room'), (b'SR', b'Study Room'), (b'CA', b'Common Area'), (b'Cf', b'Cafeteria')])),
                ('access', models.CharField(max_length=1, choices=[(b'C', b'Common'), (b'B', b'Brothers'), (b'S', b'Sisters'), (b'R', b'Restricted')])),
                ('reservable', models.BooleanField(default=False)),
            ],
        ),
    ]
