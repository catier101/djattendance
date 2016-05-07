# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20160504_1806'),
        ('accounts', '0002_statistics_trainee_trainingassistant_user'),
        ('lifestudies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('infraction', models.CharField(max_length=4, choices=[(b'AT', b'Attendance'), (b'CI', b'Cell Phone & Internet'), (b'MS', b'Missed Service'), (b'S', b'Speeding'), (b'AN', b'Alarm Noise'), (b'G', b'Guard'), (b'C', b'Curfew'), (b'M', b'Misplaced Item'), (b'HI', b'House Inspection'), (b'L', b'Library'), (b'MISC', b'Misc')])),
                ('quantity', models.PositiveSmallIntegerField()),
                ('date_assigned', models.DateTimeField(auto_now_add=True)),
                ('due', models.DateTimeField()),
                ('offense', models.CharField(default=b'RO', max_length=2, choices=[(b'MO', b'Monday Offense'), (b'RO', b'Regular Offense')])),
                ('note', models.TextField(blank=True)),
                ('trainee', models.ForeignKey(to='accounts.Trainee')),
            ],
            options={
                'ordering': ['trainee__account__lastname'],
            },
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('chapter', models.PositiveSmallIntegerField()),
                ('approved', models.BooleanField(default=False)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(to='books.Book')),
                ('discipline', models.ForeignKey(to='lifestudies.Discipline')),
            ],
            options={
                'ordering': ['approved'],
            },
        ),
    ]
