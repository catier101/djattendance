# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aputils', '0002_auto_20160504_1806'),
        ('houses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bunk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.SmallIntegerField()),
                ('position', models.CharField(max_length=1, choices=[(b'B', b'Bottom'), (b'T', b'Top'), (b'L', b'Queen-Left'), (b'R', b'Queen-Right'), (b'S', b'Single')])),
                ('length', models.CharField(default=b'R', max_length=1, choices=[(b'R', b'Regular'), (b'L', b'Long')])),
                ('frame', models.CharField(blank=True, max_length=2, null=True, choices=[(b'M', b'Metal'), (b'C', b'Cot'), (b'H', b'Wood Honey'), (b'W', b'Wood Walnut'), (b'WC', b'Wood Walnut Crown'), (b'O', b'Wood Oak'), (b'LV', b'Wood Light Vintage')])),
                ('mattress', models.CharField(max_length=50, null=True, blank=True)),
                ('guardrail', models.NullBooleanField()),
                ('ladder', models.NullBooleanField()),
                ('notes', models.TextField(null=True, blank=True)),
                ('link', models.OneToOneField(null=True, blank=True, to='houses.Bunk')),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=1, choices=[(b'B', b'Brother'), (b'S', b'Sister'), (b'C', b'Couple')])),
                ('used', models.BooleanField(default=True)),
                ('address', models.ForeignKey(to='aputils.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=4, choices=[(b'LIV', b'Living Room'), (b'BED', b'Bedroom'), (b'KIT', b'Kitchen'), (b'BATH', b'Bathroom'), (b'GAR', b'Garage'), (b'PAT', b'Patio')])),
                ('size', models.CharField(blank=True, max_length=1, null=True, choices=[(b'S', b'Small'), (b'M', b'Medium'), (b'L', b'Large')])),
                ('capacity', models.SmallIntegerField(default=0)),
                ('floor', models.SmallIntegerField(default=1)),
                ('house', models.ForeignKey(to='houses.House')),
            ],
        ),
        migrations.AddField(
            model_name='bunk',
            name='room',
            field=models.ForeignKey(to='houses.Room'),
        ),
    ]
