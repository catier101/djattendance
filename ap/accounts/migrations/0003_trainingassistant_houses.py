# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_statistics_trainee_trainingassistant_user'),
        ('houses', '0002_auto_20160504_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingassistant',
            name='houses',
            field=models.ManyToManyField(to='houses.House', blank=True),
        ),
    ]
