# Generated by Django 2.2.6 on 2019-11-03 13:32

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botmodel',
            name='names',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=['бот', 'bot']),
        ),
    ]