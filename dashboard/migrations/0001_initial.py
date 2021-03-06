# Generated by Django 3.0.5 on 2020-04-25 08:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('province_state', models.CharField(max_length=100, null=True, verbose_name='群/州')),
                ('country_region_name', models.CharField(max_length=30, verbose_name='国または地域')),
            ],
            options={
                'verbose_name': '国または地域',
                'verbose_name_plural': 'Location',
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('report_date', models.DateField(verbose_name='日付')),
                ('latitude', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(90)], verbose_name='緯度')),
                ('longitude', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(180)], verbose_name='経度')),
                ('total_cases', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='累計感染者数')),
                ('total_deaths', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='累計死亡者数')),
                ('total_recovered', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='累計完治者数')),
                ('active_cases', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='発症者数')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Location')),
            ],
            options={
                'verbose_name': '世界コロナ統計',
                'verbose_name_plural': 'World Coronavirus Report',
                'db_table': 'report',
            },
        ),
    ]
