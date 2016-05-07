# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0002_class'),
        ('books', '0002_auto_20160504_1806'),
        ('syllabus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name=b'session date')),
                ('topic', models.CharField(max_length=200)),
                ('assignment', djorm_pgarray.fields.ArrayField(default=None, null=True, blank=True)),
                ('exam', models.BooleanField(default=False)),
                ('book', models.ForeignKey(to='books.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('after', models.BooleanField(default=False)),
                ('classSyllabus', models.ForeignKey(to='classes.Class')),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='syllabus',
            field=models.ForeignKey(to='syllabus.Syllabus'),
        ),
    ]
