# Generated by Django 5.0.2 on 2024-02-18 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_marker_path_id_marker_point_id_alter_marker_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marker',
            name='seq',
        ),
    ]