# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn', models.CharField(max_length=13)),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=20)),
                ('chapters', models.SmallIntegerField(null=True, blank=True)),
                ('author', models.ManyToManyField(to='books.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='collection',
            field=models.ForeignKey(blank=True, to='books.Collection', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(to='books.Publisher'),
        ),
    ]
