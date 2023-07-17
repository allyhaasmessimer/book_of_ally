# Generated by Django 4.2.2 on 2023-07-05 19:01

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_alter_post_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                null=True, upload_to=blog.models.get_image_upload_path
            ),
        ),
    ]
