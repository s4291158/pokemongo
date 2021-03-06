# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2016-07-14 06:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Current',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_index', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=1)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Route')),
            ],
        ),
        migrations.AddField(
            model_name='current',
            name='route',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Route'),
        ),
        migrations.AlterUniqueTogether(
            name='stop',
            unique_together=set([('route', 'order')]),
        ),
    ]
