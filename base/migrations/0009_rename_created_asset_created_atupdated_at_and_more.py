# Generated by Django 4.0.2 on 2022-02-14 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alarmasset_created_at_alarmasset_updated_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='created',
            new_name='created_atupdated_at',
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='updated',
            new_name='updated_at',
        ),
    ]
