# Generated by Django 3.2.15 on 2024-02-27 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explanation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='explanation',
            name='preview',
            field=models.TextField(default='no preview'),
        ),
    ]