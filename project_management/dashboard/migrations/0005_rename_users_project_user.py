# Generated by Django 4.2.5 on 2023-10-05 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_remove_project_user_project_users'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='users',
            new_name='user',
        ),
    ]