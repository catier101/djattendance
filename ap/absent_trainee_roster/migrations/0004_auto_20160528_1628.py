# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20160504_1806'),
        ('absent_trainee_roster', '0003_auto_20160504_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='absentee',
            name='account',
        ),
        migrations.DeleteModel(
            name='Absentee',
        ),
        migrations.CreateModel(
            name='Absentee',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('accounts.user',),
        ),
    ]
