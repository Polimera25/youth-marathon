'''from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.http import HttpResponse
import os
import csv
from django.conf import settings
from .models import Race, Runner, Registration
from .forms import RegistrationForm


def landing(request):
    # --- Gallery images ---
    gallery_path = os.path.join(settings.STATICFILES_DIRS[0], "gallery")
    images = []
    if os.path.exists(gallery_path):
        for file in os.listdir(gallery_path):
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                images.append(f"gallery/{file}")

    # --- Race categories ---
    #races = Race.objects.annotate(registered=Count('registrations')).order_by('date')

    races = Race.objects.filter(name__icontains="5k").annotate(registered=Count('registrations')).order_by('date')

    return render(request, "registrations/landing.html", {
        "gallery_images": images,
        "races": races
    })


def race_list(request):
    races = Race.objects.filter(name__icontains="5k").annotate(registered=Count('registrations')).order_by('date')
    return render(request, 'registrations/races.html', {'races': races})



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            race = form.cleaned_data['race']
            runner, _ = Runner.objects.get_or_create(
                email=form.cleaned_data['email'],
                defaults={
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'phone': form.cleaned_data.get('phone', ''),
                    'age': form.cleaned_data.get('age'),
                    'gender': form.cleaned_data.get('gender') or ''
                }
            )
            # Update runner details if changed
            runner.first_name = form.cleaned_data['first_name']
            runner.last_name = form.cleaned_data['last_name']
            runner.phone = form.cleaned_data.get('phone', '')
            runner.age = form.cleaned_data.get('age')
            runner.gender = form.cleaned_data.get('gender') or ''
            runner.save()

            Registration.objects.get_or_create(
                runner=runner,
                race=race,
                defaults={'tshirt_size': form.cleaned_data['tshirt_size'], 'paid': False}
            )
            return render(request, 'registrations/success.html', {'runner': runner, 'race': race})
    else:
        form = RegistrationForm()
    return render(request, 'registrations/register.html', {'form': form})


def participants(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    q = request.GET.get('q', '').strip()
    regs = race.registrations.select_related('runner').all().order_by('-created_at')
    if q:
        regs = regs.filter(
            Q(runner__first_name__icontains=q) |
            Q(runner__last_name__icontains=q) |
            Q(runner__email__icontains=q)
        )
    return render(request, 'registrations/participants.html', {'race': race, 'regs': regs, 'q': q})


def export_csv(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{race.name.replace(" ", "_")}_participants.csv"'
    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Phone', 'Age', 'Gender', 'T-Shirt', 'Paid', 'Registered At'])
    for reg in race.registrations.select_related('runner').all().order_by('runner__last_name'):
        r = reg.runner
        writer.writerow([
            r.first_name, r.last_name, r.email, r.phone, r.age, r.gender,
            reg.tshirt_size, 'Yes' if reg.paid else 'No', reg.created_at
        ])
    return response


def dashboard(request):
    races = Race.objects.annotate(count=Count('registrations')).order_by('date')
    total_runners = Runner.objects.count()
    total_regs = Registration.objects.count()
    return render(request, 'registrations/dashboard.html', {
        'races': races,
        'total_runners': total_runners,
        'total_regs': total_regs
    })
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.http import HttpResponse
import os
import csv
from django.conf import settings

from .models import Race, Runner, Registration
from .forms import RegistrationForm, PaymentForm


def landing(request):
    # --- Gallery images ---
    gallery_path = os.path.join(settings.STATICFILES_DIRS[0], "gallery")
    images = []
    if os.path.exists(gallery_path):
        for file in os.listdir(gallery_path):
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                images.append(f"gallery/{file}")

    # --- Race categories ---
    races = (
        Race.objects.filter(name__icontains="5k")
        .annotate(registered=Count("registrations"))
        .order_by("date")
    )

    return render(
        request,
        "registrations/landing.html",
        {"gallery_images": images, "races": races},
    )


def race_list(request):
    races = (
        Race.objects.filter(name__icontains="5k")
        .annotate(registered=Count("registrations"))
        .order_by("date")
    )
    return render(request, "registrations/races.html", {"races": races})


# ---------- STEP 1: DETAILS FORM ---------- #
def register(request):
    """
    Step 1 of registration.
    - Collects participant + race details
    - Creates/updates Runner
    - Creates/gets Registration (paid=False, no UTR yet)
    - Redirects to payment step
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            race = form.cleaned_data["race"]

            # Create or update Runner from form data
            runner, _ = Runner.objects.get_or_create(
                email=form.cleaned_data["email"],
                defaults={
                    "first_name": form.cleaned_data["first_name"],
                    "last_name": form.cleaned_data["last_name"],
                    "phone": form.cleaned_data.get("phone", ""),
                    "age": form.cleaned_data.get("age"),
                    "gender": form.cleaned_data.get("gender") or "",
                },
            )

            # Update runner details if changed
            runner.first_name = form.cleaned_data["first_name"]
            runner.last_name = form.cleaned_data["last_name"]
            runner.phone = form.cleaned_data.get("phone", "")
            runner.age = form.cleaned_data.get("age")
            runner.gender = form.cleaned_data.get("gender") or ""
            runner.save()

            # Create or get Registration
            registration, created = Registration.objects.get_or_create(
                runner=runner,
                race=race,
                defaults={
                    "tshirt_size": form.cleaned_data["tshirt_size"],
                    "paid": False,
                },
            )

            # If registration already existed, update t-shirt size and reset payment info
            if not created:
                registration.tshirt_size = form.cleaned_data["tshirt_size"]
                registration.paid = False
                registration.utr_number = None
                registration.save()

            # Go to payment step
            return redirect("registrations:payment", reg_id=registration.id)
    else:
        # Preselect race if coming from /races?race=<id>
        initial = {}
        race_id = request.GET.get("race")
        if race_id:
            initial["race"] = race_id

        form = RegistrationForm(initial=initial)

    return render(request, "registrations/register.html", {"form": form})


# ---------- STEP 2: PAYMENT PAGE ---------- #
def payment(request, reg_id):
    """
    Step 2 of registration.
    Shows QR code and collects UTR / transaction ID.
    """
    registration = get_object_or_404(Registration, pk=reg_id)

    if request.method == "POST":
        form = PaymentForm(request.POST, instance=registration)
        if form.is_valid():
            reg = form.save(commit=False)
            # Payment will be verified manually later in admin
            reg.paid = False
            reg.save()

            # Reuse your existing success page
            return render(
                request,
                "registrations/success.html",
                {"runner": reg.runner, "race": reg.race},
            )
    else:
        form = PaymentForm(instance=registration)

    return render(
        request,
        "registrations/payment.html",
        {"form": form, "registration": registration},
    )


def participants(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    q = request.GET.get("q", "").strip()
    regs = race.registrations.select_related("runner").all().order_by("-created_at")
    if q:
        regs = regs.filter(
            Q(runner__first_name__icontains=q)
            | Q(runner__last_name__icontains=q)
            | Q(runner__email__icontains=q)
        )
    return render(
        request,
        "registrations/participants.html",
        {"race": race, "regs": regs, "q": q},
    )


def export_csv(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="{race.name.replace(" ", "_")}_participants.csv"'
    )
    writer = csv.writer(response)
    writer.writerow(
        [
            "First Name",
            "Last Name",
            "Email",
            "Phone",
            "Age",
            "Gender",
            "T-Shirt",
            "Paid",
            "UTR Number",
            "Registered At",
        ]
    )
    for reg in (
        race.registrations.select_related("runner")
        .all()
        .order_by("runner__last_name")
    ):
        r = reg.runner
        writer.writerow(
            [
                r.first_name,
                r.last_name,
                r.email,
                r.phone,
                r.age,
                r.gender,
                reg.tshirt_size,
                "Yes" if reg.paid else "No",
                reg.utr_number or "",
                reg.created_at,
            ]
        )
    return response


def dashboard(request):
    races = Race.objects.annotate(count=Count("registrations")).order_by("date")
    total_runners = Runner.objects.count()
    total_regs = Registration.objects.count()
    return render(
        request,
        "registrations/dashboard.html",
        {
            "races": races,
            "total_runners": total_runners,
            "total_regs": total_regs,
        },
    )
