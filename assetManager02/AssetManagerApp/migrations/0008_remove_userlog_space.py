# Generated by Django 5.0.3 on 2024-03-26 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AssetManagerApp', '0007_alter_userlog_space'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlog',
            name='space',
        ),
    ]