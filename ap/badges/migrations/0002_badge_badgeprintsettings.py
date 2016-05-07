# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import paintstore.fields
import badges.util


class Migration(migrations.Migration):

    dependencies = [
        ('terms', '0002_term'),
        ('badges', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'T', max_length=2, choices=[(b'T', b'Trainee'), (b'S', b'Staff'), (b'XS', b'XB-Staff'), (b'X', b'XB-Trainee')])),
                ('original', models.ImageField(null=True, upload_to=badges.util._image_upload_path, blank=True)),
                ('firstname', models.CharField(max_length=50, null=True, blank=True)),
                ('middlename', models.CharField(max_length=1, null=True, blank=True)),
                ('lastname', models.CharField(max_length=50, null=True, blank=True)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('title', models.CharField(max_length=30, null=True, blank=True)),
                ('locality', models.CharField(max_length=100, null=True, blank=True)),
                ('avatar', models.CharField(max_length=255, null=True, blank=True)),
                ('deactivated', models.BooleanField(default=False)),
                ('term_created', models.ForeignKey(to='terms.Term')),
            ],
        ),
        migrations.CreateModel(
            name='BadgePrintSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banner_color', paintstore.fields.ColorPickerField(max_length=7)),
            ],
            options={
                'verbose_name': 'Badge Printing Configuration',
            },
        ),
    ]
