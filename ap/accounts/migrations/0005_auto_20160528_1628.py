# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('terms', '0002_term'),
        ('badges', '0002_badge_badgeprintsettings'),
        ('localities', '0002_locality'),
        ('schedules', '0002_auto_20160504_1806'),
        ('leaveslips', '0003_auto_20160528_1628'),
        ('houses', '0002_auto_20160504_1806'),
        ('teams', '0002_team'),
        ('web_access', '0003_auto_20160528_1628'),
        ('attendance', '0003_auto_20160528_1628'),
        ('lifestudies', '0003_auto_20160528_1628'),
        ('services', '0002_auto_20160504_1806'),
        ('aputils', '0003_auto_20160528_1628'),
        ('accounts', '0004_auto_20160504_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('maidenname', models.CharField(max_length=30, null=True, verbose_name='maiden name', blank=True)),
                ('married', models.BooleanField(default=False)),
                ('spouse', models.CharField(max_length=90, null=True, blank=True)),
                ('address', models.ForeignKey(verbose_name=b'home address', blank=True, to='aputils.Address', null=True)),
                ('bunk', models.ForeignKey(blank=True, to='houses.Bunk', null=True)),
                ('houses', models.ManyToManyField(related_name='houses', to='houses.House', blank=True)),
                ('services', models.ManyToManyField(related_name='services', to='services.Service', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='TA',
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='account',
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='address',
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='badge',
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='bunk',
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='house',
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='locality',
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='mentor',
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='spouse',
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='team',
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='term',
        ),
        migrations.RemoveField(
            model_name='trainingassistant',
            name='account',
        ),
        migrations.RemoveField(
            model_name='trainingassistant',
            name='badge',
        ),
        migrations.RemoveField(
            model_name='trainingassistant',
            name='houses',
        ),
        migrations.RemoveField(
            model_name='trainingassistant',
            name='services',
        ),
        migrations.RemoveField(
            model_name='user',
            name='maidenname',
        ),
        migrations.AddField(
            model_name='user',
            name='TA',
            field=models.ForeignKey(related_name='training_assistant', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='badge',
            field=models.ForeignKey(blank=True, to='badges.Badge', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='current_term',
            field=models.IntegerField(default=1, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='date_begin',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='date_end',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='house',
            field=models.ForeignKey(blank=True, to='houses.House', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='locality',
            field=models.ManyToManyField(to='localities.Locality', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='mentor',
            field=models.ForeignKey(related_name='mentee', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='self_attendance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='team',
            field=models.ForeignKey(blank=True, to='teams.Team', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='terms_attended',
            field=models.ManyToManyField(to='terms.Term'),
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(default='R', max_length=1, choices=[(b'T', b'Training Assistant'), (b'R', b'Regular (full-time)'), (b'S', b'Short-term (long-term)'), (b'C', b'Commuter')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='statistics',
            name='trainee',
            field=models.OneToOneField(related_name='statistics', null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Trainee',
        ),
        migrations.DeleteModel(
            name='TrainingAssistant',
        ),
        migrations.AddField(
            model_name='usermeta',
            name='user',
            field=models.OneToOneField(related_name='meta', null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Trainee',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='TrainingAssistant',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('accounts.user',),
        ),
    ]
