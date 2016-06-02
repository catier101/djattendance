# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_access', '0002_webrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='webrequest',
            name='urgent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='webrequest',
            name='comments',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
