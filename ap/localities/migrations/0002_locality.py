# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aputils', '0002_auto_20160504_1806'),
        ('localities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.ForeignKey(to='aputils.City')),
            ],
            options={
                'verbose_name_plural': 'localities',
            },
        ),
    ]
