# Generated by Django 4.1.13 on 2025-04-11 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='auther',
            new_name='author',
        ),
    ]
