# Generated by Django 3.0.3 on 2020-02-16 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200216_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='resourcetype',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tagvalue',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='volumetype',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
    ]
