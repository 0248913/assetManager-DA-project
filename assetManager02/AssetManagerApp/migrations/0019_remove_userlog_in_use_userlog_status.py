# Generated by Django 5.0.3 on 2024-05-25 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AssetManagerApp", "0018_userlog_in_use"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userlog",
            name="in_use",
        ),
        migrations.AddField(
            model_name="userlog",
            name="status",
            field=models.CharField(
                choices=[("in_use", "In Use"), ("in_storage", "In Storage")],
                default="in_storage",
                max_length=20,
            ),
        ),
    ]