# Generated by Django 5.0.2 on 2024-02-29 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_alter_marker_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='marker',
            name='pip_dimeter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='marker',
            name='pip_type',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
