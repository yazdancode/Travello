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


class PassengerDetailView(View):
    template_name = "sentdex/sample.html"
    payment_template = "sentdex/payment.html"
    RegisterFormSet = formset_factory(RegisterForm, extra=1)
    
    def get(self, request, city_name):
        formset = self.RegisterFormSet()
        return render(
            request,
            self.template_name,
            {"formset": formset, "city_name": city_name}
        )

    def post(self, request, city_name):
        formset = self.RegisterFormSet(request.POST)
        if formset.is_valid():
            trip_date = datetime.strptime(request.POST["trip_date"], "%Y-%m-%d").date()
            current_date = datetime.now().date()

            if trip_date < current_date:
                return redirect("index")
            trip_obj = PassengerDetail.objects.get(Trip_id=3)
            request.session["trip_reference_id"] = trip_obj.trip_reference_id
            request.session["n"] = formset.total_form_count()
            price = request.session.get("price", 0)
            city = request.session.get("city", city_name)
            username = request.user.get_username()
            for form in formset:
                PassengerDetail.objects.create(
                    trip_reference_id=trip_obj.trip_reference_id,
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    age=form.cleaned_data["age"],
                    trip_date=trip_date,
                    payment=price,
                    username=username,
                    city=city,
                )
            trip_obj.trip_reference_id += 1
            trip_obj.save()
            num_persons = formset.total_form_count()
            total_price = num_persons * price
            gst = round(total_price * 0.18, 2)
            final_total = total_price + gst
            request.session["pay_amount"] = final_total
            return render(
                request,
                self.payment_template,
                {
                    "no_of_person": num_persons,
                    "price": total_price,
                    "GST": gst,
                    "final_total": final_total,
                    "city": city,
                }
            )
        else:
            return render(
                request,
                self.template_name,
                {"formset": formset, "city_name": city_name}
            )
