from django.contrib import admin
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
    list_display = ('runner','race','tshirt_size','paid','created_at')
    list_filter = ('race','paid','tshirt_size')
    search_fields = ('runner__first_name','runner__last_name','runner__email')
