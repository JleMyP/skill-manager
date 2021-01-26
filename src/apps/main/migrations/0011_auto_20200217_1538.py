# Generated by Django 3.0.3 on 2020-02-17 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_tag_simple'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportedResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата-время создания')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('provider', models.PositiveIntegerField(choices=[(1, 'GitHub'), (2, 'Chrome'), (3, 'VK')], verbose_name='Провайдер')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('raw_data', models.TextField(blank=True, null=True, verbose_name='Сырые данные')),
                ('is_ignored', models.BooleanField(default=False, verbose_name='В игноре')),
            ],
            options={
                'verbose_name': 'Импортированный ресурс',
                'verbose_name_plural': 'Импортированные ресурсы',
                'default_related_name': 'imported_resources',
            },
        ),
        migrations.AddField(
            model_name='resource',
            name='imported_resource',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resource', to='main.ImportedResource', verbose_name='Импортированный ресурс'),
        ),
    ]