# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activitystatistics',
            fields=[
                ('idactivitystatistics', models.AutoField(serialize=False, primary_key=True)),
                ('activityname', models.CharField(max_length=300)),
                ('count', models.IntegerField()),
            ],
            options={
                'db_table': 'activitystatistics',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Appruncount',
            fields=[
                ('idappruncount', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('appversion', models.CharField(max_length=45, blank=True)),
                ('runcount', models.BigIntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'appruncount',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Appruncount2',
            fields=[
                ('idappruncount', models.AutoField(serialize=False, primary_key=True)),
                ('datetime', models.DateTimeField(null=True, blank=True)),
                ('appversion', models.CharField(max_length=45, blank=True)),
                ('appruncount', models.BigIntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'appruncount2',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Appstatistics',
            fields=[
                ('idappstatistics', models.AutoField(serialize=False, primary_key=True)),
                ('appversion', models.CharField(max_length=45)),
                ('count', models.IntegerField()),
                ('pid', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'appstatistics',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField()),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(unique=True, max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=75)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
                ('image_path', models.CharField(max_length=260, blank=True)),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('idcomment', models.AutoField(serialize=False, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('comment', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'comments',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Countrystatistics',
            fields=[
                ('idcountrystatistics', models.AutoField(serialize=False, primary_key=True)),
                ('countryname', models.CharField(max_length=45)),
                ('count', models.IntegerField()),
            ],
            options={
                'db_table': 'countrystatistics',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Devicestatistics',
            fields=[
                ('iddevicestatistics', models.AutoField(serialize=False, primary_key=True)),
                ('devicename', models.CharField(max_length=75, blank=True)),
                ('count', models.IntegerField()),
            ],
            options={
                'db_table': 'devicestatistics',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Errors',
            fields=[
                ('iderror', models.AutoField(serialize=False, primary_key=True)),
                ('rank', models.IntegerField()),
                ('autodetermine', models.IntegerField()),
                ('status', models.IntegerField(null=True, blank=True)),
                ('numofinstances', models.IntegerField()),
                ('createdate', models.DateTimeField()),
                ('lastdate', models.DateTimeField()),
                ('callstack', models.TextField()),
                ('errorname', models.CharField(max_length=10000, blank=True)),
                ('errorclassname', models.CharField(max_length=300)),
                ('linenum', models.CharField(max_length=45)),
                ('errorweight', models.IntegerField(null=True, blank=True)),
                ('recur', models.IntegerField(null=True, blank=True)),
                ('eventpath', models.TextField(blank=True)),
                ('wifion', models.IntegerField()),
                ('gpson', models.IntegerField()),
                ('mobileon', models.IntegerField()),
                ('totalmemusage', models.IntegerField()),
                ('gain1', models.FloatField(null=True, blank=True)),
                ('gain2', models.FloatField(null=True, blank=True)),
            ],
            options={
                'db_table': 'errors',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Eventpaths',
            fields=[
                ('ideventpaths', models.AutoField(serialize=False, primary_key=True)),
                ('ins_count', models.IntegerField(null=True, blank=True)),
                ('datetime', models.DateTimeField(null=True, blank=True)),
                ('classname', models.CharField(max_length=300, blank=True)),
                ('methodname', models.CharField(max_length=300, blank=True)),
                ('linenum', models.IntegerField(null=True, blank=True)),
                ('depth', models.IntegerField(null=True, blank=True)),
                ('label', models.CharField(max_length=300, blank=True)),
            ],
            options={
                'db_table': 'eventpaths',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstanceLog',
            fields=[
                ('idinstance', models.IntegerField(serialize=False, primary_key=True)),
                ('log', models.TextField(blank=True)),
                ('savetime', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'instancelog',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Instances',
            fields=[
                ('idinstance', models.AutoField(serialize=False, primary_key=True)),
                ('ins_count', models.IntegerField(null=True, blank=True)),
                ('sdkversion', models.CharField(max_length=45, blank=True)),
                ('appversion', models.CharField(max_length=45, blank=True)),
                ('osversion', models.CharField(max_length=75, blank=True)),
                ('kernelversion', models.CharField(max_length=45, blank=True)),
                ('appmemmax', models.CharField(max_length=45, blank=True)),
                ('appmemfree', models.CharField(max_length=45, blank=True)),
                ('appmemtotal', models.CharField(max_length=45, blank=True)),
                ('country', models.CharField(max_length=45, blank=True)),
                ('datetime', models.DateTimeField(null=True, blank=True)),
                ('locale', models.CharField(max_length=45, blank=True)),
                ('mobileon', models.IntegerField(null=True, blank=True)),
                ('gpson', models.IntegerField(null=True, blank=True)),
                ('wifion', models.IntegerField(null=True, blank=True)),
                ('device', models.CharField(max_length=75, blank=True)),
                ('rooted', models.IntegerField(null=True, blank=True)),
                ('scrheight', models.IntegerField(null=True, blank=True)),
                ('scrwidth', models.IntegerField(null=True, blank=True)),
                ('scrorientation', models.IntegerField(null=True, blank=True)),
                ('sysmemlow', models.CharField(max_length=45, blank=True)),
                ('log_path', models.CharField(max_length=260, blank=True)),
                ('batterylevel', models.IntegerField(null=True, blank=True)),
                ('availsdcard', models.IntegerField(null=True, blank=True)),
                ('xdpi', models.FloatField(null=True, blank=True)),
                ('ydpi', models.FloatField(null=True, blank=True)),
                ('callstack', models.TextField(blank=True)),
                ('dump_path', models.CharField(max_length=260, blank=True)),
                ('lastactivity', models.CharField(max_length=300, blank=True)),
                ('pid', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'instances',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Osstatistics',
            fields=[
                ('idosstatistics', models.AutoField(serialize=False, primary_key=True)),
                ('osversion', models.CharField(max_length=75, blank=True)),
                ('count', models.IntegerField()),
                ('pid', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'osstatistics',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proguardmap',
            fields=[
                ('idproguardmap', models.AutoField(serialize=False, primary_key=True)),
                ('appversion', models.CharField(max_length=45, blank=True)),
                ('filename', models.CharField(max_length=45, blank=True)),
                ('uploadtime', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'proguardmap',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('pid', models.AutoField(serialize=False, primary_key=True)),
                ('apikey', models.CharField(unique=True, max_length=10)),
                ('platform', models.IntegerField()),
                ('name', models.CharField(max_length=45)),
                ('stage', models.IntegerField()),
                ('category', models.IntegerField(null=True, blank=True)),
                ('timezone', models.CharField(max_length=45, blank=True)),
            ],
            options={
                'db_table': 'projects',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectSummary',
            fields=[
                ('instanceCount', models.IntegerField()),
                ('pid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('apikey', models.CharField(max_length=10)),
                ('owner_uid', models.CharField(max_length=10)),
                ('platform', models.IntegerField()),
                ('stage', models.IntegerField()),
            ],
            options={
                'db_table': 'projectsummary',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('idsession', models.BigIntegerField(serialize=False, primary_key=True)),
                ('appversion', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'session',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sessionevent',
            fields=[
                ('idsessionevent', models.AutoField(serialize=False, primary_key=True)),
                ('datetime', models.DateTimeField(null=True, blank=True)),
                ('classname', models.CharField(max_length=300, blank=True)),
                ('methodname', models.CharField(max_length=300, blank=True)),
                ('linenum', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'sessionevent',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sofiles',
            fields=[
                ('idsofiles', models.AutoField(serialize=False, primary_key=True)),
                ('appversion', models.CharField(max_length=45)),
                ('versionkey', models.CharField(max_length=45, blank=True)),
                ('filename', models.CharField(max_length=45, blank=True)),
                ('uploaded', models.CharField(max_length=45, blank=True)),
            ],
            options={
                'db_table': 'sofiles',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('idtag', models.AutoField(serialize=False, primary_key=True)),
                ('tag', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'tags',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('idviewer', models.AutoField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'viewer',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CountrysbyApp',
            fields=[
                ('count', models.IntegerField(serialize=False, primary_key=True)),
                ('country', models.CharField(max_length=45, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Erba',
            fields=[
                ('activity', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('sum', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Erbd',
            fields=[
                ('device', models.CharField(max_length=45, serialize=False, primary_key=True)),
                ('sum', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Erbv',
            fields=[
                ('appversion', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('osversion', models.CharField(max_length=255)),
                ('sum', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ErbvApps',
            fields=[
                ('appversion', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('sum', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ErrorbyRank',
            fields=[
                ('iderrorbyrank', models.IntegerField(serialize=False, primary_key=True)),
                ('errorcount', models.IntegerField(null=True, blank=True)),
                ('errorrank', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ErrorsbyApp',
            fields=[
                ('errorcount', models.IntegerField(serialize=False, primary_key=True)),
                ('appversion', models.CharField(max_length=45, blank=True)),
                ('errorday', models.CharField(max_length=45, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ErrorStatistics',
            fields=[
                ('iderrorstatistics', models.IntegerField(serialize=False, primary_key=True)),
                ('keyname', models.CharField(max_length=45, blank=True)),
                ('count', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstanceCountModel',
            fields=[
                ('iderror', models.IntegerField(serialize=False, primary_key=True)),
                ('count', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LoginApprunCount',
            fields=[
                ('pid', models.IntegerField(serialize=False, primary_key=True)),
                ('count', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LoginErrorCountModel',
            fields=[
                ('pid', models.IntegerField(serialize=False, primary_key=True)),
                ('count', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SessionbyApp',
            fields=[
                ('idsessionbyapp', models.IntegerField(serialize=False, primary_key=True)),
                ('runcount', models.IntegerField(null=True, blank=True)),
                ('appversion', models.CharField(max_length=45, blank=True)),
                ('sessionday', models.CharField(max_length=45, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TotalSession',
            fields=[
                ('appversion', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('total', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
