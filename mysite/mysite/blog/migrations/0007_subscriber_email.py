# Generated by Django 4.2.2 on 2023-07-05 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_remove_subscriber_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriber",
            name="email",
            field=models.EmailField(default="", max_length=254),
        ),
    ]