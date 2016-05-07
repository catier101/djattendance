# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terms', '0002_term'),
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=4, choices=[(b'MAIN', b'Main'), (b'1YR', b'1st Year'), (b'2YR', b'2nd Year'), (b'AFTN', b'Afternoon')])),
                ('term', models.ForeignKey(to='terms.Term')),
            ],
            options={
                'verbose_name_plural': 'classes',
            },
        ),
    ]
