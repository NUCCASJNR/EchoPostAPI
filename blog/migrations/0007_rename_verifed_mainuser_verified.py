# Generated by Django 5.0.1 on 2024-01-22 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_rename_veriifed_mainuser_verifed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mainuser',
            old_name='verifed',
            new_name='verified',
        ),
    ]
