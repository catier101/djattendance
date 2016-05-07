# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal_seating', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('capacity', models.IntegerField(null=True)),
                ('location', models.CharField(max_length=2, choices=[(b'W', b'West Cafeteria'), (b'M', b'Main Cafeteria'), (b'S', b'South Cafeteria'), (b'SE', b'Southeast Cafeteria')])),
                ('genderType', models.CharField(max_length=1, choices=[(b'B', b'Brother'), (b'S', b'Sister')])),
            ],
        ),
    ]
