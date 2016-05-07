# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Group')),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('startDate', models.DateField(verbose_name=b'start date')),
                ('endDate', models.DateField(verbose_name=b'end date')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Group')),
                ('description', models.TextField(null=True, blank=True)),
                ('isActive', models.BooleanField(default=True)),
                ('workload', models.IntegerField()),
                ('category', models.ForeignKey(to='services.Category')),
            ],
            bases=('auth.group',),
        ),
        migrations.AddField(
            model_name='period',
            name='service',
            field=models.ManyToManyField(to='services.Service'),
        ),
    ]
