# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aputils', '0002_auto_20160504_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='trainee',
            field=models.ForeignKey(related_name='vehicles', blank=True, to='accounts.Trainee', null=True),
        ),
    ]
