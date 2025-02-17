# Generated by Django 3.2.25 on 2025-01-22 07:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('develop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Develop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github_id', models.CharField(blank=True, default='', max_length=100)),
                ('repository_name', models.CharField(blank=True, default='', max_length=100)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Settings',
        ),
    ]
