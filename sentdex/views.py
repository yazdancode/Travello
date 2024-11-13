from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from sentdex.forms import RegisterForm
from sentdex.models import Destination, DetailedDescription


class DestinationView(View):
    template_name = "sentdex/index.html"

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
        return render(request, self.template_name, {"dests": dests, "dest1": dest1})


class RegisterView(View):
    template_name = "sentdex/register.html"

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            username = form.cleaned_data.get("email")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            place = form.cleaned_data.get("place")
            search = form.cleaned_data.get("search")

            if User.objects.filter(username=username).exists():
                messages.info(request, "نام کاربری قبلاً استفاده شده است")
                return render(request, self.template_name, {"form": form})
            elif User.objects.filter(email=email).exists():
                messages.info(request, "ایمیل قبلاً استفاده شده است")
                return render(request, self.template_name, {"form": form})
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    place=place,
                    search=search,
                )
                user.save()
                messages.success(request, "ثبت نام با موفقیت انجام شد. لطفاً وارد شوید.")
                return redirect("login")
        else:
            messages.error(request, "اطلاعات وارد شده معتبر نیست")
            return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = "sentdex/login.html"
    success_template_name = "index.html"

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.info(request, "با موفقیت وارد سیستم شد")
                content = (
                    f"سلام {request.user.first_name} {request.user.last_name}\n"
                    "شما وارد سایت ما شده اید. در ارتباط باشید و به سفر ادامه دهید."
                )
                dests = Destination.objects.all()
                return render(
                    request,
                    self.success_template_name,
                    {"dests": dests, "content": content},
                )
            else:
                messages.info(request, "اعتبارنامه نامعتبر")
                return redirect("login")
        else:
            messages.error(request, "لطفاً فرم را با اطلاعات معتبر پر کنید.")
            return render(request, self.template_name, {"form": form})


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect("index")


@method_decorator(login_required(login_url="login"), name="dispatch")
class DestinationListView(ListView):
    model = DetailedDescription
    template_name = "sentdex/travel_destination.html"
    context_object_name = "dests"

    def get_queryset(self):
        city_name = self.kwargs["city_name"]
        return DetailedDescription.objects.filter(country=city_name)


class DestinationDetailsView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, city_name):
        dest = get_object_or_404(DetailedDescription, dest_id=city_name)
        request.session["price"] = dest.price
        request.session["city"] = city_name
        return render(request, "sentdex/destination_details.html", {"dest": dest})
