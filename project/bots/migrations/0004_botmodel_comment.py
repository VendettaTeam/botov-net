# Generated by Django 2.2.6 on 2019-11-03 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0003_auto_20191103_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='botmodel',
            name='comment',
            field=models.CharField(default='', max_length=256),
        ),
    ]