# Generated by Django 3.0.3 on 2020-02-16 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200215_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcetype',
            name='description',
            field=models.TextField(default='', verbose_name='Описание'),
            preserve_default=False,
        ),
    ]