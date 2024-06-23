# Generated by Django 5.0.6 on 2024-06-23 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CenterType',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('center_type_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('product_id', models.CharField(max_length=100)),
                ('appointment_type_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SmileCenter',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('id_external', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100, null=True)),
                ('street', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=50)),
                ('neighborhood', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100, null=True)),
                ('apt', models.CharField(max_length=50)),
                ('time_table', models.CharField(max_length=150)),
                ('region', models.CharField(max_length=100, null=True)),
                ('cp', models.CharField(max_length=20, null=True)),
                ('country', models.CharField(max_length=100, null=True)),
                ('center_type_name', models.CharField(max_length=100)),
                ('services', models.CharField(max_length=1000)),
                ('zone', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SmileCenterByCenterType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smile_center_id', models.IntegerField()),
                ('center_type_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SmileCenterByServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smile_center_id', models.IntegerField()),
                ('services_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SmileCenterByZones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smile_center_id', models.IntegerField()),
                ('zone_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('zone', models.CharField(max_length=100)),
            ],
        ),
    ]
