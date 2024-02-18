# Generated by Django 5.0.2 on 2024-02-18 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_marker_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='marker',
            name='path_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='marker',
            name='point_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='marker',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
