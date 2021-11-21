from django.contrib.admin import AdminSite
from django.contrib import admin

from .models import *

AdminSite.index_title = 'Администрация сайта'
AdminSite.site_title = 'Передержка животных'
AdminSite.site_header = 'Передержка животных'


class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'phone_number', 'email')


class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'weight', 'breed', 'recommendations', 'client')


class RequestAdmin(admin.ModelAdmin):
    list_display = ('pet', 'description')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('request', 'created_at', 'duration', 'status')


class AgreementAdmin(admin.ModelAdmin):
    list_display = ('order', 'description', 'price')


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'phone_number', 'email', 'position')


class CarAdmin(admin.ModelAdmin):
    list_display = ('numbers', 'mark_n_model', 'color', 'worker')


class TransportEventAdmin(admin.ModelAdmin):
    list_display = ('order', 'timestamp_start', 'timestamp_end', 'description')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('order', 'created_at', 'description', 'video', 'image')


admin.site.register(Client, ClientAdmin)
admin.site.register(Pet, PetAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Agreement, AgreementAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(TransportEvent, TransportEventAdmin)
admin.site.register(Report, ReportAdmin)
