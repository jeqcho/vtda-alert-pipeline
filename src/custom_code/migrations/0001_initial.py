# Generated by Django 4.2.4 on 2023-09-24 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tom_targets', '0020_alter_targetname_created_alter_targetname_modified'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostGalaxy',
            fields=[
                ('ID', models.IntegerField(help_text='Object ID of galaxy', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='NED name of galaxy', max_length=100, unique=True)),
                ('ra', models.FloatField(help_text='Right ascension of galaxy')),
                ('dec', models.FloatField(help_text='Declination of galaxy')),
                ('catalog', models.CharField(default='../data/ghost/GHOST.csv', help_text='CSV file where all columns are stored.', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTargetList',
            fields=[
                ('targetlist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tom_targets.targetlist')),
                ('query', models.CharField(help_text="This project's query submission string for ANTARES.", max_length=1000)),
                ('tns', models.BooleanField(help_text='Whether to query TNS catalog')),
                ('sn_type', models.CharField(help_text='The supernova type to check for.', max_length=100)),
            ],
            options={
                'ordering': ('-created', 'name'),
            },
            bases=('tom_targets.targetlist',),
        ),
        migrations.CreateModel(
            name='TargetAux',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_offset', models.FloatField(help_text='Angular offset between target and host galaxy.', null=True)),
                ('host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aux_objects', to='custom_code.hostgalaxy')),
                ('target', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='aux_info', to='tom_targets.target')),
            ],
        ),
        migrations.CreateModel(
            name='HostGalaxyName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Alias')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='The time at which this host name was created.')),
                ('modified', models.DateTimeField(auto_now=True, help_text='The time at which this host name was changed in the TOM database.', verbose_name='Last Modified')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aliases', to='custom_code.hostgalaxy')),
            ],
        ),
        migrations.AddConstraint(
            model_name='hostgalaxy',
            constraint=models.CheckConstraint(check=models.Q(('ra__gte', 0.0), ('ra__lte', 360.0)), name='host_ra_range'),
        ),
        migrations.AddConstraint(
            model_name='hostgalaxy',
            constraint=models.CheckConstraint(check=models.Q(('dec__gte', -180.0), ('dec__lte', 180.0)), name='host_dec_range'),
        ),
        migrations.CreateModel(
            name='QuerySet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The query name', max_length=100)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='custom_code.projecttargetlist')),
            ],
        ),
        migrations.CreateModel(
            name='QueryTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antares_name', models.CharField(help_text='The tag name when queried from ANTARES', max_length=100)),
                ('queryset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_code.queryset')),
            ],
        ),
        migrations.CreateModel(
            name='QueryProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antares_name', models.CharField(help_text='The property name when queried from ANTARES', max_length=100)),
                ('min_value', models.FloatField(help_text='Minimum value', null=True)),
                ('max_value', models.FloatField(help_text='Maximum value', null=True)),
                ('categorical', models.BooleanField(default=False, help_text='Whether property value is categorical (as opposed to continuous)')),
                ('target_value', models.CharField(help_text='Target property value if categorical', max_length=100, null=True)),
                ('queryset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_code.queryset')),
            ],
        ),
        migrations.AddConstraint(
            model_name='querytag',
            constraint=models.UniqueConstraint(fields=('queryset', 'antares_name'), name='no_repeat_query_tags'),
        ),
        migrations.AddConstraint(
            model_name='queryproperty',
            constraint=models.UniqueConstraint(fields=('queryset', 'antares_name'), name='no_repeat_query_properties'),
        ),
    ]
