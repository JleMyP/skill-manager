# Generated by Django 3.0.3 on 2020-02-21 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20200217_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='skills', to='main.Skill', verbose_name='Батька'),
        ),
    ]
