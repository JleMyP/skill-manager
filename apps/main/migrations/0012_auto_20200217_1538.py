# Generated by Django 3.0.3 on 2020-02-17 15:38

from django.db import migrations


def move_raw_data(apps, schema_editor):
    from ..models import ImportedResource  # для Provider
    resource_class = apps.get_model('main', 'Resource')
    imported_resource_class = apps.get_model('main', 'ImportedResource')

    qs = resource_class.objects.all()
    for resource in qs:
        resource.imported_resource = imported_resource_class.objects.create(
            provider=ImportedResource.Provider.GITHUB,
            name=resource.name,
            description=resource.description,
            raw_data=resource.raw_data,
        )
        resource.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20200217_1538'),
    ]

    operations = [
        migrations.RunPython(move_raw_data),
    ]
