# Generated by Django 3.2.15 on 2023-04-04 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explanation', '0007_alter_explanation_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='explanation',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='explanation',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]