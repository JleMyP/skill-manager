# Generated by Django 3.0.3 on 2020-02-17 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20200217_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='simple',
        ),
        migrations.AddField(
            model_name='tagvalue',
            name='is_default',
            field=models.BooleanField(default=False, verbose_name='Значение по умолчанию'),
        ),
    ]