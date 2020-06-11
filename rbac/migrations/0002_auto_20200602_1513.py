# Generated by Django 3.0.6 on 2020-06-02 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='group',
        ),
        migrations.RemoveField(
            model_name='role',
            name='permissions',
        ),
        migrations.RemoveField(
            model_name='user',
            name='roles',
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
        migrations.DeleteModel(
            name='PermissionGroup',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]