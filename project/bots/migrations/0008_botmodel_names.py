# Generated by Django 2.2.6 on 2019-10-19 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0007_auto_20191016_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='botmodel',
            name='names',
            field=models.TextField(null=True),
        ),
    ]
    
