# Generated by Django 3.0.6 on 2020-06-02 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0003_auto_20200602_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='action',
        ),
        migrations.RemoveField(
            model_name='role',
            name='group',
        ),
    ]