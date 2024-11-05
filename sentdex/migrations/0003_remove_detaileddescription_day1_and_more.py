# Generated by Django 5.1.3 on 2024-11-05 14:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sentdex", "0002_detaileddescription_remove_destination_img1_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="detaileddescription",
            name="day1",
        ),
        migrations.RemoveField(
            model_name="detaileddescription",
            name="day2",
        ),
        migrations.RemoveField(
            model_name="detaileddescription",
            name="day3",
        ),
        migrations.RemoveField(
            model_name="detaileddescription",
            name="day4",
        ),
        migrations.RemoveField(
            model_name="detaileddescription",
            name="day5",
        ),
        migrations.RemoveField(
            model_name="detaileddescription",
            name="day6",
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
    ]
