# Generated by Django 5.1.4 on 2024-12-17 13:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], max_length=6),
        ),
    ]