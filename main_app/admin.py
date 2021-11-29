from django.contrib.admin import AdminSite
from django.contrib import admin

from .models import *

AdminSite.index_title = 'Администрация сайта'
AdminSite.site_title = 'Ресторан'
AdminSite.site_header = 'Ресторан'


class RegularCustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'phone_number', 'client_status')
    list_filter = ('client_status',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('employer', 'cost_of_the_order', 'status')
    list_filter = ('status',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'employer':
            kwargs["queryset"] = Staff.objects.filter(position__position='Официант')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('order',)


class StaffAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'position', 'phone_number', 'work_experience')
    list_filter = ('position', 'work_experience')
    search_fields = ('last_name', 'first_name')


class PositionsAdmin(admin.ModelAdmin):
    list_display = ('position', 'responsibilities')
    list_filter = ('position',)
    search_fields = ('responsibilities',)


class DishesAdmin(admin.ModelAdmin):
    list_display = ('name', 'workpiece')
    list_filter = ('name',)


class WorkpiecesAdmin(admin.ModelAdmin):
    list_display = ('name', 'ingredients', 'date_of_creation', 'expiration_date')
    list_filter = ('name', 'date_of_creation', 'expiration_date')
    search_fields = ('ingredients',)


class BatchAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'ingredients', 'number_of_positions', 'delivery_date')
    list_filter = ('supplier', 'delivery_date',)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'phone_number')
    search_fields = ('last_name', 'first_name',)


admin.site.register(RegularCustomer, RegularCustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Positions, PositionsAdmin)
admin.site.register(Dishes, DishesAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Workpieces, WorkpiecesAdmin)
admin.site.register(Receipt, ReceiptAdmin)

#
# class ClientAdmin(admin.ModelAdmin):
#     list_display = ('last_name', 'first_name', 'middle_name', 'phone_number', 'email')
#
#
# class PetAdmin(admin.ModelAdmin):
#     list_display = ('name', 'type', 'weight', 'breed', 'recommendations', 'client')
#
#
# class RequestAdmin(admin.ModelAdmin):
#     list_display = ('pet', 'description')
#     list_filter = ('pet',)
#     search_fields = ('description',)
#
#
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('request', 'created_at', 'duration', 'status')
#     list_filter = ('created_at', 'status')
#     search_fields = ('duration', 'status')
#
#
# class AgreementAdmin(admin.ModelAdmin):
#     list_display = ('order', 'description', 'price')
#
#
# class WorkerAdmin(admin.ModelAdmin):
#     list_display = ('last_name', 'first_name', 'middle_name', 'phone_number', 'email', 'position')
#
#
# class CarAdmin(admin.ModelAdmin):
#     list_display = ('numbers', 'mark_n_model', 'color', 'worker')
#
#
# class TransportEventAdmin(admin.ModelAdmin):
#     list_display = ('order', 'timestamp_start', 'timestamp_end', 'description')
#
#
# class ReportAdmin(admin.ModelAdmin):
#     list_display = ('order', 'created_at', 'description', 'video', 'image')
#
#
# admin.site.register(Client, ClientAdmin)
# admin.site.register(Pet, PetAdmin)
# admin.site.register(Request, RequestAdmin)
# admin.site.register(Order, OrderAdmin)
# admin.site.register(Agreement, AgreementAdmin)
# admin.site.register(Worker, WorkerAdmin)
# admin.site.register(Car, CarAdmin)
# admin.site.register(TransportEvent, TransportEventAdmin)
# admin.site.register(Report, ReportAdmin)
