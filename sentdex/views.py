from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from sentdex.forms import RegisterForm
from sentdex.models import Destination, DetailedDescription


class DestinationView(View):
    template_name = 'sentdex/index.html'
    
    @staticmethod
    def get_destinations_with_descriptions():
        dest1 = []
        for i in range(6):
            try:
                temp = DetailedDescription.objects.get(dest_id=(i + 1) * 2)
                dest1.append(temp)
            except ObjectDoesNotExist:
                dest1.append(None)
        return dest1

    def get(self, request):
        dests = Destination.objects.all()
        dest1 = self.get_destinations_with_descriptions()
        return render(request, self.template_name, {'dests': dests, 'dest1': dest1})
    
    
class RegisterView(View):
    template_name = 'sentdex/register.html'

    def get(self, request):
        # form = RegisterForm()
        return render(request, self.template_name)

    def post(self, request):
        form = RegisterForm  # Correct usage of request.POST (uppercase)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                messages.info(request, 'نام کاربری قبلاً استفاده شده است')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'ایمیل قبلاً استفاده شده است')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                messages.success(request, 'ثبت نام با موفقیت انجام شد. لطفاً وارد شوید.')
                return redirect('login')
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نیست')
            return render(request, self.template_name, {'form': form})

