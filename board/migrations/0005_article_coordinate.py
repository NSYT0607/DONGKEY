# Generated by Django 2.0.1 on 2018-04-19 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_article_hit'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='coordinate',
            field=models.CharField(default=1, max_length=100, verbose_name='좌표'),
            preserve_default=False,
        ),
    ]
