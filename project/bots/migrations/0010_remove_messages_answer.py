# Generated by Django 2.2.6 on 2019-11-02 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0009_messages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='answer',
        ),
    ]
