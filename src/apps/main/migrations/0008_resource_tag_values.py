# Generated by Django 3.0.3 on 2020-02-16 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200216_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='tag_values',
            field=models.ManyToManyField(blank=True, related_name='resources', to='main.TagValue', verbose_name='Метки со значениями'),
        ),
    ]
