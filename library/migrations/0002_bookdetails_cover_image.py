# Generated by Django 5.1.7 on 2025-03-29 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookdetails",
            name="cover_image",
            field=models.ImageField(blank=True, null=True, upload_to="covers/"),
        ),
    ]
