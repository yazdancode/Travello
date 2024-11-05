# Generated by Django 5.1.3 on 2024-11-05 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Destination",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        primary_key=True, serialize=False, verbose_name="شناسه"
                    ),
                ),
                ("country", models.CharField(max_length=256, verbose_name="کشور")),
                ("img1", models.ImageField(upload_to="pics", verbose_name="تصویر یک")),
                ("img2", models.ImageField(upload_to="pics", verbose_name="تصویر دو")),
                ("number", models.IntegerField(default=2, verbose_name="شماره")),
            ],
            options={
                "verbose_name": "مقصد",
                "verbose_name_plural": "مقصد",
            },
        ),
    ]
