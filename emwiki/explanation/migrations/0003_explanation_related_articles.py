# Generated by Django 3.2.25 on 2024-05-24 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_remove_article_related_documents'),
        ('explanation', '0002_explanation_preview'),
    ]

    operations = [
        migrations.AddField(
            model_name='explanation',
            name='related_articles',
            field=models.ManyToManyField(related_name='explanations', to='article.Article'),
        ),
    ]
