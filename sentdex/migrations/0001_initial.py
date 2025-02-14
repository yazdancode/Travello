# Generated by Django 5.1.3 on 2024-11-06 05:14

import django.db.models.deletion
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
                ("number", models.IntegerField(default=2, verbose_name="شماره")),
            ],
            options={
                "verbose_name": "مقصد",
                "verbose_name_plural": "مقصد",
            },
        ),
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
            ],
            options={
                "verbose_name": "توضیحات مقصد",
                "verbose_name_plural": "توضیحات مقصد",
            },
        ),
        migrations.CreateModel(
            name="PassengerDetail",
            fields=[
                (
                    "trip_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="شناسه سفر"
                    ),
                ),
                (
                    "trip_same_id",
                    models.IntegerField(default=1, verbose_name="همان شناسه سفر"),
                ),
                ("first_name", models.CharField(max_length=15, verbose_name="نام")),
                (
                    "last_name",
                    models.CharField(max_length=15, verbose_name="نام خانوادگی"),
                ),
                ("age", models.IntegerField(default=10, verbose_name="سن")),
                (
                    "username",
                    models.CharField(max_length=10, verbose_name="نام کاربری"),
                ),
                ("trip_date", models.DateField(verbose_name="تاریخ سفر")),
                ("payment", models.IntegerField(default=50, verbose_name="پرداخت")),
                ("city", models.CharField(max_length=20, verbose_name="شهر")),
                (
                    "pay_done",
                    models.BooleanField(default=False, verbose_name="پرداخت انجام شد"),
                ),
            ],
            options={
                "verbose_name": "جزئیات مسافر",
                "verbose_name_plural": "جزئیات مسافران",
            },
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
            name="DailyPlan",
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
                ("day_number", models.IntegerField(verbose_name="روز شماره")),
                ("plan", models.CharField(max_length=200, verbose_name="برنامه روز")),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="daily_plans",
                        to="sentdex.detaileddescription",
                        verbose_name="مقصد",
                    ),
                ),
            ],
            options={
                "verbose_name": "برنامه روزانه",
                "verbose_name_plural": "برنامه\u200cهای روزانه",
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
