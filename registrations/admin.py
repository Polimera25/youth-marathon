'''from django.contrib import admin
from .models import Race, Runner, Registration

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name','date','distance_km','capacity','location')
    search_fields = ('name','location')
    list_filter = ('date',)

@admin.register(Runner)
class RunnerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','phone','age','gender')
    search_fields = ('first_name','last_name','email')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('runner','race','tshirt_size','paid','utr_number','created_at')
    list_filter = ('race','paid','tshirt_size')
    search_fields = ('runner__first_name','runner__last_name','runner__email','utr_number',)
    # ---- Admin Actions ----
    actions = ["mark_as_paid", "mark_as_unpaid"]

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(paid=True)
        self.message_user(request, f"✔ {updated} registration(s) marked as PAID.")
    mark_as_paid.short_description = "Mark selected registrations as PAID"

    def mark_as_unpaid(self, request, queryset):
        updated = queryset.update(paid=False)
        self.message_user(request, f"❌ {updated} registration(s) marked as NOT paid.")
    mark_as_unpaid.short_description = "Mark selected registrations as NOT PAID"
'''

from django.contrib import admin
from .models import Race, Runner, Registration


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "distance_km", "capacity", "location")
    search_fields = ("name", "location")
    list_filter = ("date",)


@admin.register(Runner)
class RunnerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "age", "gender")
    search_fields = ("first_name", "last_name", "email")
    

# --------- ACTION FUNCTIONS (outside the class) --------- #

@admin.action(description="Mark selected registrations as PAID")
def mark_as_paid(modeladmin, request, queryset):
    updated = queryset.update(paid=True)
    modeladmin.message_user(request, f"✔ {updated} registration(s) marked as PAID.")


@admin.action(description="Mark selected registrations as NOT PAID")
def mark_as_unpaid(modeladmin, request, queryset):
    updated = queryset.update(paid=False)
    modeladmin.message_user(request, f"❌ {updated} registration(s) marked as NOT PAID.")


# --------- REGISTRATION ADMIN --------- #

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("runner", "race", "tshirt_size", "paid", "utr_number", "created_at")
    list_filter = ("race", "paid", "tshirt_size")
    search_fields = (
        "runner__first_name",
        "runner__last_name",
        "runner__email",
        "utr_number",
    )

    actions = [mark_as_paid, mark_as_unpaid]
