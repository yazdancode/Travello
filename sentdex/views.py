from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos.libgeos import GEOSCoordSeq_t
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from sentdex.forms import RegisterForm
from django.forms import formset_factory
from sentdex.models import Destination, DetailedDescription, PassengerDetail
from datetime import datetime


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


class SearchView(View):
    template_name = "sentdex/destination_details.html"

    def get(self, request, *args, **kwargs):
        try:
            place = request.session.get("place")
            dest = DetailedDescription.objects.get(dest_name=place)
            return render(request, self.template_name, {"dest": dest})
        except DetailedDescription.DoesNotExist:
            messages.info(request, "Place not found")
            return redirect("index")


def pessanger_datail_def(request, city_name):
    RegisterFormSet = formset_factory(RegisterForm, extra=1)
    if request.method == "POST":
        formset = RegisterFormSet(request.POST)
        if formset.is_valid():
            temp_date = datetime.strptime(request.POST["trip_date"], "%Y-%m-%d").date()
            date = datetime.now().date()
            if temp_date < date:
                return redirect("index")

            obj = PassengerDetail.objects.get(Trip_id=3)
            pipo_id = obj.trip_reference_id
            request.session["trip_reference_id"] = pipo_id
            price = request.session["price"]
            city = request.session["city"]
            temp_date = datetime.strptime(request.POST["trip_date"], "%Y-%m-%d").date()
            usernameget = request.user.get_username()
            request.session["n"] = formset.total_form_count()
            for i in range(0, formset.total_form_count()):
                form = formset.forms[i]
                t = PassengerDetail(
                    trip_reference_id=pipo_id,
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    age=form.cleaned_data["age"],
                    trip_date=temp_date,
                    payment=price,
                    username=usernameget,
                    city=city,
                )
                t.save()
            obj.trip_reference_id = pipo_id + 1
            obj.save()
            no_of_person = formset.total_form_count()
            price = no_of_person * price
            GST = price * 0.18
            GST = float("{:.2f}".format(GST))
            final_total = GST + price
            request.session["pay_amount"] = final_total
            return render(
                request,
                "sentdex/payment.html",
                {
                    "no_of_person": no_of_person,
                    "price": price,
                    "GST": GST,
                    "final_total": final_total,
                    "city": city,
                },
            )
        else:
            formset = RegisterFormSet()

            return render(
                request,
                "sentdex/sample.html",
                {
                    "formset": formset,
                    "city_name": city_name,
                },
            )
