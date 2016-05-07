# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current', models.BooleanField(default=False)),
                ('season', models.CharField(default=None, max_length=6, choices=[(b'Spring', b'Spring'), (b'Fall', b'Fall')])),
                ('year', models.PositiveSmallIntegerField()),
                ('start', models.DateField(verbose_name=b'start date')),
                ('end', models.DateField(verbose_name=b'end date')),
            ],
        ),
    ]
