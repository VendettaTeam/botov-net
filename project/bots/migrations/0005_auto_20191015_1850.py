# Generated by Django 2.2.6 on 2019-10-15 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0004_botmodel_group_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botmodel',
            name='group_id',
            field=models.BigIntegerField(),
        ),
    ]