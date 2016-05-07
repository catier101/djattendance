# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('teams', '0002_team'),
        ('houses', '0002_auto_20160504_1806'),
        ('accounts', '0003_trainingassistant_houses'),
        ('badges', '0002_badge_badgeprintsettings'),
        ('terms', '0002_term'),
        ('localities', '0002_locality'),
        ('services', '0002_auto_20160504_1806'),
        ('aputils', '0002_auto_20160504_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingassistant',
            name='services',
            field=models.ManyToManyField(to='services.Service', blank=True),
        ),
        migrations.AddField(
            model_name='trainee',
            name='TA',
            field=models.ForeignKey(blank=True, to='accounts.TrainingAssistant', null=True),
        ),
        migrations.AddField(
            model_name='trainee',
            name='account',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='trainee',
            name='address',
            field=models.ForeignKey(verbose_name=b'home address', blank=True, to='aputils.Address', null=True),
        ),
        migrations.AddField(
            model_name='trainee',
            name='badge',
            field=models.ForeignKey(blank=True, to='badges.Badge', null=True),
        ),
        migrations.AddField(
            model_name='trainee',
            name='bunk',
            field=models.ForeignKey(blank=True, to='houses.Bunk', null=True),
        ),
        migrations.AddField(
            model_name='trainee',
            name='house',
            field=models.ForeignKey(blank=True, to='houses.House', null=True),
        ),
        migrations.AddField(
            model_name='trainee',
            name='locality',
            field=models.ManyToManyField(to='localities.Locality', blank=True),
        ),
        migrations.AddField(
            model_name='trainee',
            name='mentor',
            field=models.ForeignKey(related_name='mentee', blank=True, to='accounts.Trainee', null=True),
        ),
        migrations.AddField(
            model_name='trainee',
            name='spouse',
            field=models.OneToOneField(null=True, blank=True, to='accounts.Trainee'),
        ),
        migrations.AddField(
            model_name='trainee',
            name='team',
            field=models.ForeignKey(blank=True, to='teams.Team', null=True),
        ),
        migrations.AddField(
            model_name='trainee',
            name='term',
            field=models.ManyToManyField(to='terms.Term'),
        ),
        migrations.AddField(
            model_name='statistics',
            name='trainee',
            field=models.OneToOneField(related_name='statistics', null=True, blank=True, to='accounts.Trainee'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
