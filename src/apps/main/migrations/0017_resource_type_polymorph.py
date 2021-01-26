# Generated by Django 3.0.4 on 2020-03-10 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('main', '0016_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportedResourceRepo',
            fields=[
                ('importedresource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.ImportedResource')),
            ],
            options={
                'abstract': False,
            },
            bases=('main.importedresource',),
        ),
        migrations.RemoveField(
            model_name='importedresource',
            name='provider',
        ),
        migrations.AddField(
            model_name='importedresource',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_main.importedresource_set+', to='contenttypes.ContentType'),
        ),
    ]