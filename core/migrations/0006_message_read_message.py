# Generated by Django 3.2.6 on 2021-08-28 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_message_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read_message',
            field=models.BooleanField(default=False),
        ),
    ]
