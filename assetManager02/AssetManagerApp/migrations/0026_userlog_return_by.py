# Generated by Django 5.0.3 on 2024-05-26 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AssetManagerApp", "0025_alter_userlog_last_changed_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="userlog",
            name="return_by",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]