# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dailybread', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('ref', models.CharField(max_length=255)),
                ('timestamp', models.TimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('submitted_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
