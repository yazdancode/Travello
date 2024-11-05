# Generated by Django 5.1.3 on 2024-11-05 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sentdex", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DetailedDescription",
            fields=[
                (
                    "dest_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="شناسه مقصد"
                    ),
                ),
                ("country", models.CharField(max_length=256, verbose_name="کشور")),
                ("days", models.IntegerField(default=5, verbose_name="روز")),
                ("price", models.IntegerField(default=20000, verbose_name="قیمت")),
                ("rating", models.IntegerField(default=5, verbose_name="رتبه بندی")),
                ("dest_name", models.CharField(max_length=25, verbose_name="نام مقصد")),
                ("desc", models.TextField(verbose_name="توصیف")),
                (
                    "day1",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="روز اول"
                    ),
                ),
                (
                    "day2",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="روز دوم"
                    ),
                ),
                (
                    "day3",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="روز سوم"
                    ),
                ),
                (
                    "day4",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="روز چهارم"
                    ),
                ),
                (
                    "day5",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="روز پنجم"
                    ),
                ),
                (
                    "day6",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="روز ششم"
                    ),
                ),
            ],
            options={
                "verbose_name": "توضیحات مقصد",
                "verbose_name_plural": "توضیحات مقصد",
            },
        ),
        migrations.RemoveField(
            model_name="destination",
            name="img1",
        ),
        migrations.RemoveField(
            model_name="destination",
            name="img2",
        ),
        migrations.CreateModel(
            name="DestinationImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="pics", verbose_name="تصویر")),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="sentdex.destination",
                        verbose_name="مقصد",
                    ),
                ),
            ],
            options={
                "verbose_name": "تصویر مقصد",
                "verbose_name_plural": "تصاویر مقصد",
            },
        ),
        migrations.CreateModel(
            name="DetailedDescriptionImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="pics", verbose_name="تصویر")),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="sentdex.detaileddescription",
                        verbose_name="توضیحات مقصد",
                    ),
                ),
            ],
            options={
                "verbose_name": "تصویر توضیحات مقصد",
                "verbose_name_plural": "تصاویر توضیحات مقصد",
            },
        ),
    ]
