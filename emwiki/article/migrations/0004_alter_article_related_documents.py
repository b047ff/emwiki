# Generated by Django 3.2.25 on 2024-05-20 05:57

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_article_related_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='related_documents',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=list, size=None),
        ),
    ]
