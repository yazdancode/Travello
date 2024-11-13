from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    User,
)  # فرض بر این است که از مدل User استفاده می‌کنید.
import re


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        min_length=10,
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                "class": "input100",
                "type": "text",
                "placeholder": "نام کاربری خود را تایپ کنید",
            }
        ),
    )
    first_name = forms.CharField(
        max_length=255,
        label="نام",
        widget=forms.TextInput(
            attrs={
                "class": "input--style-4",
                "type": "text",
                "placeholder": "نام خود را تایپ کنید",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=255,
        label="نام خانوادگی",
        widget=forms.TextInput(
            attrs={
                "class": "input--style-4",
                "type": "text",
                "placeholder": "نام خانوادگی خود را تایپ کنید",
            }
        ),
    )
    password = forms.CharField(
        min_length=8,
        max_length=16,
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "class": "input--style-4",
                "type": "password",
                "placeholder": "رمز عبور خود را تایپ کنید",
            }
        ),
    )
    password_to_accept = forms.CharField(
        min_length=8,
        max_length=16,
        label="تأیید رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "class": "input--style-4",
                "type": "password",
                "placeholder": "رمز عبور خود را دوباره تایپ کنید",
            }
        ),
    )
    phone_number = forms.CharField(
        max_length=13,
        label="شماره تلفن",
        widget=forms.TextInput(
            attrs={
                "class": "input--style-4",
                "type": "text",
                "maxlength": "13",
                "placeholder": "شماره تلفن خود را تایپ کنید",
            }
        ),
    )
    email = forms.EmailField(
        max_length=50,
        label="ایمیل",
        widget=forms.TextInput(
            attrs={
                "class": "input--style-4",
                "type": "email",
                "placeholder": "ایمیل خود را تایپ کنید",
            }
        ),
    )

    place = forms.CharField(
        max_length=256,
        label="محل",
        widget=forms.TextInput(
            attrs={
                "class": "input--style-4",
                "type": "text",
                "placeholder": "کجا بریم؟",
            }
        ),
    )

    search = forms.CharField(
        max_length=256,
        label="جستجو کنید",
        widget=forms.TextInput(
            attrs={
                "class": "input--style-4",
                "type": "text",
                "placeholder": "جستجو کنید",
            }
        ),
    )
    
    age = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_to_accept = cleaned_data.get("password_to_accept")

        if password != password_to_accept:
            raise ValidationError(
                "رمزهای عبور با هم مطابقت ندارند.", code="password_mismatch"
            )

        # افزودن شرایط امنیتی برای رمز عبور
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$", password
        ):
            raise ValidationError(
                "رمز عبور باید بین ۸ تا ۱۶ کاراکتر باشد و شامل حداقل یک حرف، یک عدد، و یک کاراکتر خاص باشد.",
                code="password_complexity",
            )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "این نام کاربری قبلاً ثبت شده است.", code="username_taken"
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل قبلاً ثبت شده است.", code="email_taken")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not re.match(r"^[\u0600-\u06FF\s]+$", first_name):
            raise ValidationError(
                "نام باید فقط شامل حروف فارسی باشد.", code="invalid_first_name"
            )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not re.match(r"^[\u0600-\u06FF\s\-]+$", last_name):
            raise ValidationError(
                "نام خانوادگی باید فقط شامل حروف فارسی و خط فاصله باشد.",
                code="invalid_last_name",
            )
        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not re.match(r"^\+?(98)?9\d{9}$", phone_number):
            raise ValidationError(
                "شماره تلفن باید با +98 یا 09 شروع شود و ۱۱ رقم باشد.",
                code="invalid_phone_number",
            )
        return phone_number
