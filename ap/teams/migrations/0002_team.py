# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0002_locality'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=6, choices=[(b'CAMPUS', b'Campus'), (b'CHILD', b'Children'), (b'COM', b'Community'), (b'YP', b'Young People'), (b'I', b'Internet')])),
                ('locality', models.ForeignKey(to='localities.Locality')),
                ('superteam', models.ForeignKey(blank=True, to='teams.Team', null=True)),
            ],
        ),
    ]
