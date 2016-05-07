# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0002_badge_badgeprintsettings'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address', db_index=True)),
                ('firstname', models.CharField(max_length=30, verbose_name='first name')),
                ('lastname', models.CharField(max_length=30, verbose_name='last name')),
                ('middlename', models.CharField(max_length=30, null=True, verbose_name='middle name', blank=True)),
                ('nickname', models.CharField(max_length=30, null=True, blank=True)),
                ('maidenname', models.CharField(max_length=30, null=True, verbose_name='maiden name', blank=True)),
                ('gender', models.CharField(max_length=1, choices=[(b'B', b'Brother'), (b'S', b'Sister')])),
                ('date_of_birth', models.DateField(null=True)),
                ('phone', models.CharField(max_length=25, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latest_ls_chpt', models.CharField(max_length=400, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trainee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('type', models.CharField(max_length=1, choices=[(b'R', b'Regular (full-time)'), (b'S', b'Short-term (long-term)'), (b'C', b'Commuter')])),
                ('date_begin', models.DateField()),
                ('date_end', models.DateField(null=True, blank=True)),
                ('married', models.BooleanField(default=False)),
                ('self_attendance', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrainingAssistant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('account', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('badge', models.ForeignKey(blank=True, to='badges.Badge', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
