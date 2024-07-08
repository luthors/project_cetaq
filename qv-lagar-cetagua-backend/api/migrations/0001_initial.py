# Generated by Django 4.2.7 on 2024-03-06 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnomalyFilter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number_of_days', models.IntegerField()),
                ('tolerance', models.CharField(choices=[('ALTA', 'Alta'), ('MEDIA', 'Media'), ('BAJA', 'Baja')], default='MEDIA', max_length=10)),
                ('indicator_number', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Anomaly Filter',
                'verbose_name_plural': 'Anomaly Filters',
                'db_table': 'api_anomaly_filter',
            },
        ),
        migrations.CreateModel(
            name='Exploitation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Exploitation',
                'verbose_name_plural': 'Exploitations',
                'db_table': 'api_exploitation',
            },
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Indicator',
                'verbose_name_plural': 'Indicators',
                'db_table': 'api_indicator',
            },
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('geojson', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exploitation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.exploitation')),
            ],
            options={
                'verbose_name': 'Map',
                'verbose_name_plural': 'Maps',
                'db_table': 'api_map',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('map', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.map')),
            ],
            options={
                'verbose_name': 'Sector',
                'verbose_name_plural': 'Sectors',
                'db_table': 'api_sector',
            },
        ),
        migrations.CreateModel(
            name='IndicatorThreshold',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(null=True)),
                ('meanWeekDays', models.IntegerField(null=True)),
                ('meanSurrounding', models.FloatField(null=True)),
                ('hours', models.IntegerField(null=True)),
                ('tolerance', models.FloatField(null=True)),
                ('movingAverageDays', models.IntegerField(null=True)),
                ('fixedAverageDays', models.IntegerField(null=True)),
                ('weightAverage', models.FloatField(null=True)),
                ('weightDeviation', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('anomaly_filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.anomalyfilter')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.indicator')),
            ],
            options={
                'verbose_name': 'Indicator Threshold',
                'verbose_name_plural': 'Indicator Thresholds',
                'db_table': 'api_indicator_threshold',
            },
        ),
        migrations.CreateModel(
            name='HydraulicPerformance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('bimester', models.IntegerField()),
                ('hp_total_percentage', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.sector')),
            ],
            options={
                'verbose_name': 'Hydraulic Performance',
                'verbose_name_plural': 'Hydraulic Performances',
                'db_table': 'api_hydraulic_performance',
            },
        ),
        migrations.CreateModel(
            name='HPVariables',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('contract_number', models.IntegerField()),
                ('liters_supplied', models.FloatField()),
                ('percentage_adjustment', models.FloatField()),
                ('percentage_telereading', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hydraulic_performance', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.hydraulicperformance')),
            ],
            options={
                'verbose_name': 'HP Variables',
                'verbose_name_plural': 'HP Variables',
                'db_table': 'api_hp_variables',
            },
        ),
        migrations.CreateModel(
            name='HPExpectedVariables',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hp_expected', models.FloatField()),
                ('supplied_expected', models.FloatField()),
                ('registed_expected', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hydraulic_performance', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.hydraulicperformance')),
            ],
            options={
                'verbose_name': 'HP Expected Variables',
                'verbose_name_plural': 'HP Expected Variables',
                'db_table': 'api_hp_expected_variables',
            },
        ),
        migrations.AddField(
            model_name='anomalyfilter',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.sector'),
        ),
    ]