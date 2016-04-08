# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='roll',
            options={'permissions': (('attendance_all', 'Can'),)},
        ),
    ]
