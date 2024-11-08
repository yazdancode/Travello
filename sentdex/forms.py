from django import forms
import re


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                "class": "input100",
                "type": "text",
                "min_length": "10",
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
                "placeholder": "رمز عبور خود را تایپ کنید"
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
            }
        ),
    )
    phone_number = forms.CharField(
        max_length=14,
        label="شماره تلفن",
        widget=forms.TextInput(
            attrs={"class": "input--style-4", "type": "text", "maxlength": "12"}
        ),
    )
    email = forms.EmailField(
        max_length=50,
        label="ایمیل",
        widget=forms.TextInput(attrs={"class": "input--style-4", "type": "email"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_to_accept = cleaned_data.get("password_to_accept")

        if password != password_to_accept:
            raise forms.ValidationError("رمزهای عبور با هم مطابقت ندارند.")

        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$", password):
            raise forms.ValidationError(
                "رمز عبور باید حداقل یک حرف بزرگ و یک عدد داشته باشد."
            )

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not re.match(r"^[\u0600-\u06FF\s]+$", first_name):
            raise forms.ValidationError("نام باید فقط شامل حروف فارسی باشد.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not re.match(r"^[\u0600-\u06FF\s\-]+$", last_name):
            raise forms.ValidationError(
                "نام خانوادگی باید فقط شامل حروف فارسی و خط فاصله باشد."
            )
        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not re.match(r"^\+?(\d{1,4})?(\d{10})$", phone_number):
            raise forms.ValidationError("شماره تلفن معتبر نمی‌باشد.")
        return phone_number
