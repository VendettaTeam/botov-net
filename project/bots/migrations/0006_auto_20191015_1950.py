# Generated by Django 2.2.6 on 2019-10-15 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0005_auto_20191015_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botmodel',
            name='group_id',
            field=models.BigIntegerField(unique=True),
        ),
    ]
