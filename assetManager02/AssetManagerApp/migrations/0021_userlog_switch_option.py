# Generated by Django 5.0.3 on 2024-05-25 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AssetManagerApp", "0020_remove_userlog_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="userlog",
            name="switch_option",
            field=models.BooleanField(default=False),
        ),
    ]