# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20160504_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainee',
            name='office_id',
            field=models.PositiveIntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='date_begin',
            field=models.DateField(null=True, blank=True),
        ),
    ]
