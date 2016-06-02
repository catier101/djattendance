# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lifestudies', '0002_discipline_summary'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discipline',
            options={'ordering': ['trainee__lastname']},
        ),
        migrations.AlterField(
            model_name='discipline',
            name='trainee',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
