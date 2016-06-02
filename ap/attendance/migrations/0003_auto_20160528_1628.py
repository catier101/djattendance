# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_roll'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roll',
            old_name='timestamp',
            new_name='last_modified',
        ),
        migrations.RenameField(
            model_name='roll',
            old_name='monitor',
            new_name='submitted_by',
        ),
    ]
