# Generated by Django 3.2.7 on 2021-11-17 17:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_auto_20211017_1705'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='function',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AddField(
            model_name='function',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
    ]
