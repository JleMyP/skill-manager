# Generated by Django 2.2.10 on 2020-02-15 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20191120_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='image',
            field=models.TextField(blank=True, null=True, verbose_name='Картинка'),
        ),
    ]
