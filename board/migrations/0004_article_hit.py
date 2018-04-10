# Generated by Django 2.0.1 on 2018-04-09 05:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0003_auto_20180226_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='hit',
            field=models.ManyToManyField(related_name='hit_article_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
