# Generated by Django 3.2.6 on 2021-08-27 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
