from django.db import models
from django.utils.translation import gettext_lazy as _


class Destination(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="شناسه")
    country = models.CharField(max_length=256, verbose_name="کشور")
    number = models.IntegerField(default=2, verbose_name="شماره")

    class Meta:
        verbose_name = _("مقصد")
        verbose_name_plural = _("مقصد")

    def __str__(self):
        return f"Destination {self.id} - {self.country}"


class DestinationImage(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="مقصد",
    )
    image = models.ImageField(upload_to="pics", verbose_name="تصویر")

    class Meta:
        verbose_name = _("تصویر مقصد")
        verbose_name_plural = _("تصاویر مقصد")

    def __str__(self):
        return f"Image for {self.destination.country}"


class DetailedDescription(models.Model):
    dest_id = models.AutoField(primary_key=True, verbose_name="شناسه مقصد")
    country = models.CharField(max_length=256, verbose_name="کشور")
    days = models.IntegerField(default=5, verbose_name="روز")
    price = models.IntegerField(default=20000, verbose_name="قیمت")
    rating = models.IntegerField(default=5, verbose_name="رتبه بندی")
    dest_name = models.CharField(max_length=25, verbose_name="نام مقصد")
    desc = models.TextField(verbose_name="توصیف")

    class Meta:
        verbose_name = _("توضیحات مقصد")
        verbose_name_plural = _("توضیحات مقصد")

    def __str__(self):
        return f"{self.dest_name} - {self.country}"


class DailyPlan(models.Model):
    destination = models.ForeignKey(
        DetailedDescription,
        on_delete=models.CASCADE,
        related_name="daily_plans",
        verbose_name="مقصد",
    )
    day_number = models.IntegerField(verbose_name="روز شماره")
    plan = models.CharField(max_length=200, verbose_name="برنامه روز")

    class Meta:
        verbose_name = _("برنامه روزانه")
        verbose_name_plural = _("برنامه‌های روزانه")

    def __str__(self):
        return f"{self.destination.dest_name} - روز {self.day_number}"


class DetailedDescriptionImage(models.Model):
    destination = models.ForeignKey(
        DetailedDescription,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="توضیحات مقصد",
    )
    image = models.ImageField(upload_to="pics", verbose_name="تصویر")

    class Meta:
        verbose_name = _("تصویر توضیحات مقصد")
        verbose_name_plural = _("تصاویر توضیحات مقصد")

    def __str__(self):
        return f"Image for {self.destination.dest_name} - {self.destination.country}"


class PassengerDetail(models.Model):
    trip_id = models.AutoField(primary_key=True, verbose_name="شناسه سفر")
    trip_same_id = models.IntegerField(default=1, verbose_name="همان شناسه سفر")
    first_name = models.CharField(max_length=15, verbose_name="نام")
    last_name = models.CharField(max_length=15, verbose_name="نام خانوادگی")
    age = models.IntegerField(default=10, verbose_name="سن")
    username = models.CharField(max_length=10, verbose_name="نام کاربری")
    trip_date = models.DateField(verbose_name="تاریخ سفر")
    payment = models.IntegerField(default=50, verbose_name="پرداخت")
    city = models.CharField(max_length=20, verbose_name="شهر")
    pay_done = models.BooleanField(default=False, verbose_name="پرداخت انجام شد")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.trip_id}"

    class Meta:
        verbose_name = "جزئیات مسافر"
        verbose_name_plural = "جزئیات مسافران"
