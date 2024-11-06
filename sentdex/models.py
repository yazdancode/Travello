from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Destination(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="شناسه")
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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=20000, verbose_name="قیمت")
    rating = models.IntegerField(default=5, verbose_name="رتبه بندی")
    name = models.CharField(max_length=25, verbose_name="نام مقصد")
    description = models.TextField(verbose_name="توصیف")

    class Meta:
        verbose_name = _("توضیحات مقصد")
        verbose_name_plural = _("توضیحات مقصد")

    def __str__(self):
        return f"{self.name} - {self.country}"


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
        return f"{self.destination.name} - روز {self.day_number}"


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
        return f"Image for {self.destination.name} - {self.destination.country}"


class PassengerDetail(models.Model):
    trip_id = models.AutoField(primary_key=True, verbose_name="شناسه سفر")
    trip_reference_id = models.IntegerField(default=1, verbose_name="همان شناسه سفر")
    first_name = models.CharField(max_length=15, verbose_name="نام")
    last_name = models.CharField(max_length=15, verbose_name="نام خانوادگی")
    age = models.IntegerField(default=10, verbose_name="سن")
    username = models.CharField(max_length=10, verbose_name="نام کاربری")
    trip_date = models.DateField(verbose_name="تاریخ سفر")
    payment = models.DecimalField(max_digits=10, decimal_places=2, default=50, verbose_name="پرداخت")
    city = models.CharField(max_length=20, verbose_name="شهر")
    pay_done = models.BooleanField(default=False, verbose_name="پرداخت انجام شد")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.trip_id}"

    class Meta:
        verbose_name = _("جزئیات مسافر")
        verbose_name_plural = _("جزئیات مسافران")


class Card(models.Model):
    card_number = models.CharField(primary_key=True, max_length=16, verbose_name='شماره کارت')
    expiry_month = models.CharField(max_length=2, verbose_name='ماه انقضا')
    expiry_year = models.CharField(max_length=2, verbose_name='سال انقضا')
    cvv = models.CharField(max_length=3, verbose_name='CVV')
    balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='موجودی')
    email = models.EmailField(max_length=50, default='yshabanei@gmail.com')

    def __str__(self):
        return f"{self.card_number} - {self.email}"

    class Meta:
        verbose_name = _("کارت")
        verbose_name_plural = _("کارت‌ها")


class NetBanking(models.Model):
    username = models.CharField(primary_key=True, max_length=16, verbose_name='نام کاربری')
    password = models.CharField(max_length=14, verbose_name='رمز عبور')
    bank = models.CharField(max_length=25, verbose_name='بانک')
    balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='تعادل')

    def __str__(self):
        return f"{self.username} - {self.balance}"

    class Meta:
        verbose_name = _("نت بانکینگ")
        verbose_name_plural = _("نت بانکینگ")


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True, verbose_name='شناسه تراکنش')
    username = models.CharField(max_length=10, verbose_name="نام کاربری")
    trip_reference_id = models.IntegerField(default=1, verbose_name="شناسه سفر")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مقدار")
    status = models.CharField(default="Failed", max_length=15, verbose_name="وضعیت")
    payment_method = models.CharField(max_length=15, blank=True, verbose_name="روش پرداخت")
    date_time = models.DateTimeField(default=timezone.now, verbose_name="تاریخ و زمان")

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.username}"

    class Meta:
        verbose_name = _("تراکنش")
        verbose_name_plural = _("تراکنش‌ها")
