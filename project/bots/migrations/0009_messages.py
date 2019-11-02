# Generated by Django 2.2.6 on 2019-11-02 08:17

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0008_botmodel_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(default='', max_length=1024)),
                ('answer', django.contrib.postgres.fields.jsonb.JSONField()),
                ('bot_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bots.BotModel')),
            ],
        ),
    ]
