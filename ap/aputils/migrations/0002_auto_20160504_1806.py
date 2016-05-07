# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_statistics_trainee_trainingassistant_user'),
        ('aputils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address1', models.CharField(max_length=150)),
                ('address2', models.CharField(max_length=150, blank=True)),
                ('zip_code', models.PositiveIntegerField()),
                ('zip4', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('details', models.CharField(max_length=150, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='EmergencyInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('relation', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=15)),
                ('phone2', models.CharField(max_length=15, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(blank=True, unique=True, max_length=2, choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming'), (b'PR', b'Puerto Rico')])),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', models.CharField(max_length=20)),
                ('make', models.CharField(max_length=30)),
                ('model', models.CharField(max_length=30)),
                ('year', models.PositiveSmallIntegerField()),
                ('license_plate', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=20)),
                ('capacity', models.PositiveSmallIntegerField()),
                ('trainee', models.ForeignKey(blank=True, to='accounts.Trainee', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HomeAddress',
            fields=[
                ('address_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='aputils.Address')),
                ('trainee', models.ForeignKey(to='accounts.Trainee')),
            ],
            bases=('aputils.address',),
        ),
        migrations.AddField(
            model_name='emergencyinfo',
            name='address',
            field=models.ForeignKey(to='aputils.Address'),
        ),
        migrations.AddField(
            model_name='emergencyinfo',
            name='trainee',
            field=models.OneToOneField(null=True, blank=True, to='accounts.Trainee'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(blank=True, to='aputils.State', null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(to='aputils.City'),
        ),
    ]
