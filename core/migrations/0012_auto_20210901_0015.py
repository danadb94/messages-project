# Generated by Django 3.2.6 on 2021-08-31 21:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0011_alter_readmessage_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readmessage',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.message'),
        ),
        migrations.AlterField(
            model_name='readmessage',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
