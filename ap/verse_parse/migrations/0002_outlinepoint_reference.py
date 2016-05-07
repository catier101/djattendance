# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verse_parse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutlinePoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.PositiveSmallIntegerField()),
                ('string', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book', models.CharField(max_length=25)),
                ('chapter', models.PositiveSmallIntegerField(null=True)),
                ('verse', models.PositiveSmallIntegerField(null=True)),
                ('end_chapter', models.PositiveSmallIntegerField(null=True)),
                ('end_verse', models.PositiveSmallIntegerField(null=True)),
                ('outline_point', models.ForeignKey(to='verse_parse.OutlinePoint')),
            ],
        ),
    ]
