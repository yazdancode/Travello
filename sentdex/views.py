import random
from datetime import datetime

from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView

from sentdex.forms import RegisterForm
from sentdex.models import (
    Card,
    Destination,
    DetailedDescription,
    NetBanking,
    PassengerDetail,
    Transaction,
)


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
            dest = DetailedDescription.objects.get(name=place)
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
            request, self.template_name, {"formset": formset, "city_name": city_name}
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
                },
            )
        else:
            return render(
                request,
                self.template_name,
                {"formset": formset, "city_name": city_name},
            )


class UpcomingTripsView(View):
    template_name = "sentdex/upcoming_trip.html"

    def get(self, request, *args, **kwargs):
        username = request.user.get_username()
        data = datetime.now().date()
        person = PassengerDetail.objects.filter(
            username=username, pay_done=1, Trip_date__gte=data
        )
        return render(request, self.template_name, {"person": person})


class CardPaymentView(View):
    @method_decorator(login_required(login_url="login"))
    def post(self, request, *args, **kwargs):
        card_no = request.POST.get("card_number")
        pay_method = "Debit card"
        MM = request.POST.get("MM")
        YY = request.POST.get("YY")
        CVV = request.POST.get("cvv")
        request.session["dcard"] = card_no

        try:
            card = Card.objects.get(
                card_number=card_no,
                pay_method=pay_method,
                expiry_month=MM,
                expiry_year=YY,
                cvv=CVV,
            )
            balance = card.balance
            request.session["total_balance"] = balance
            mail1 = card.email

            if int(balance) >= int(request.session.get("pay_amount", 0)):
                rno = random.randint(100000, 999999)
                request.session["OTP"] = rno
                amt = request.session["pay_amount"]
                username = request.user.get_username()
                user = User.objects.get(username=username)
                mail_id = user.email
                msg = f"Your OTP For Payment of ₹{amt} is {rno}"

                send_mail(
                    "OTP for Debit card Payment",
                    msg,
                    "yshabanei@gmail.com",
                    [mail_id],
                    fail_silently=False,
                )
                return render(request, "sentdex/OTP.html")
            else:
                messages.error(request, "موجودی کافی نیست.")
                return render(request, "sentdex/wrongdata.html")

        except Card.DoesNotExist:
            messages.error(request, "اطلاعات کارت نادرست است.")
            return render(request, "sentdex/wrongdata.html")


@method_decorator(login_required(login_url="login"), name="dispatch")
class NetBankingPaymentView(View):
    template_success = "sentdex/confirmetion_page.html"
    template_error = "sentdex/wrongdata.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get("cardNumber")
        password = request.POST.get("pass")
        bank_name = request.POST.get("banks")
        username_get = request.user.get_username()
        trip_same_id = request.session.get("trip_reference_id")
        amt = int(request.session.get("pay_amount", 0))
        pay_method = "Net Banking"

        try:
            net_banking_account = NetBanking.objects.get(
                username=username, password=password, Bank=bank_name
            )
            balance = net_banking_account.balance
            request.session["total_balance"] = balance

            if int(balance) >= amt:
                remaining_balance = balance - amt
                net_banking_account.balance = remaining_balance
                net_banking_account.save(update_fields=["balance"])
                transaction = Transaction(
                    username=username,
                    trip_reference_id=trip_same_id,
                    amount=amt,
                    payment_method=pay_method,
                    status="Successful",
                )
                transaction.save()

                return render(request, self.template_success)

            else:
                transaction = Transaction(
                    username=username_get,
                    trip_reference_id=trip_same_id,
                    amount=amt,
                    payment_method=pay_method,
                    status="Failed",
                )
                transaction.save()

                return render(request, self.template_error)

        except NetBanking.DoesNotExist:
            return render(request, self.template_error)


class OTPVerificationView(LoginRequiredMixin, FormView):
    login_url = "login"
    template_name = "sentdex/otp_verification.html"
    success_url = "/confirmation/"

    def post(self, request, *args, **kwargs):
        try:
            otp = int(request.POST.get("otp"))
            usernameget = request.user.get_username()
            trip_reference_id = request.session.get("trip_reference_id")
            amt = int(request.session.get("pay_amount", 0))
            pay_method = "Debit card"
            if otp == int(request.session.get("OTP", 0)):
                del request.session["OTP"]
                total_balance = int(request.session.get("total_balance", 0))
                rem_balance = total_balance - amt
                card = Card.objects.get(card_number=request.session.get("dcard"))
                card.Balance = rem_balance
                card.save(update_fields=["balance"])
                transaction = Transaction(
                    username=usernameget,
                    trip_reference_id=trip_reference_id,
                    amount=amt,
                    payment_method=pay_method,
                    status="Successful",
                )
                transaction.save()
                passengers = PassengerDetail.objects.filter(
                    trip_reference_id=trip_reference_id
                )
                for passenger in passengers:
                    passenger.pay_done = 1
                    passenger.save(update_fields=["pay_done"])

                return render(request, "sentdex/confirmation_page.html")
            else:
                transaction = Transaction(
                    username=usernameget,
                    trip_reference_id=trip_reference_id,
                    amount=amt,
                    payment_method=pay_method,
                    status="Failed",
                )
                transaction.save()

                return render(request, "sentdex/wrong_OTP.html")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect("otp_verification")


class DataFetchView(LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "sentdex/passenger_detail.html"
    context_object_name = "passenger_details"

    def get_queryset(self):
        username = self.request.user.get_username()
        return PassengerDetail.objects.filter(username=username)


class AboutView(TemplateView):
    template_name = "sentdex/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "About Us"
        return context


class BlogView(TemplateView):
    template_name = "sentdex/blog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Blog Us"
        return context


class SingleBlogView(TemplateView):
    template_name = "sentdex/single-blog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Single Blog US"
        return context


class ContactView(TemplateView):
    template_name = "sentdex/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Single Blog US"
        return context
