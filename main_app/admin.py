from django.contrib.admin import AdminSite
from django.contrib import admin

from .models import *

AdminSite.index_title = 'Site administration'
AdminSite.site_title = 'Overexposure of animals'
AdminSite.site_header = 'Overexposure of animals'


#
#
# class MediaImageInline(admin.TabularInline):
#     model = MediaImage
#     extra = 0
#
#
# class MediaAudioInline(admin.TabularInline):
#     model = MediaAudio
#     extra = 0
#
#
# class MediaLinkInline(admin.TabularInline):
#     model = MediaLink
#     extra = 0
#
#
# class MediaImageAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             self.exclude = ()
#             return qs
#         self.exclude = ()
#         return qs.filter(artifact__room__exposition=request.user.exposition)
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if request.user.is_superuser:
#             if db_field.name == "artifact":
#                 kwargs["queryset"] = Artifact.objects.all()
#             return super().formfield_for_foreignkey(db_field, request, **kwargs)
#         if db_field.name == "artifact":
#             kwargs["queryset"] = Artifact.objects.filter(room__exposition=request.user.exposition)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
#
#
# class MediaAudioAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             self.exclude = ()
#             return qs
#         self.exclude = ()
#         return qs.filter(artifact__room__exposition=request.user.exposition)
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if request.user.is_superuser:
#             if db_field.name == "artifact":
#                 kwargs["queryset"] = Artifact.objects.all()
#             return super().formfield_for_foreignkey(db_field, request, **kwargs)
#         if db_field.name == "artifact":
#             kwargs["queryset"] = Artifact.objects.filter(room__exposition=request.user.exposition)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
#
#
# class MediaLinkAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             self.exclude = ()
#             return qs
#         self.exclude = ()
#         return qs.filter(artifact__room__exposition=request.user.exposition)
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if request.user.is_superuser:
#             if db_field.name == "artifact":
#                 kwargs["queryset"] = Artifact.objects.all()
#             return super().formfield_for_foreignkey(db_field, request, **kwargs)
#         if db_field.name == "artifact":
#             kwargs["queryset"] = Artifact.objects.filter(room__exposition=request.user.exposition)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
#
#
# class TicketAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         if not obj.id:
#             obj.exposition = request.user.exposition
#         obj.save()
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             self.exclude = ()
#             return qs
#         self.exclude = ('token', 'visited_rooms', 'exposition')
#         return qs.filter(exposition=request.user.exposition)
#
#
# class ArtifactAdmin(admin.ModelAdmin):
#     # list_display = ('name', 'id', 'room', 'recognition_image')
#     list_display = ('name', 'id', 'room')
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             self.exclude = ()
#             return qs
#         self.exclude = ('uid', 'recognition_image')
#         return qs.filter(room__exposition=request.user.exposition)
#
#     inlines = [
#         MediaImageInline,
#         MediaAudioInline,
#         MediaLinkInline,
#     ]
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if request.user.is_superuser:
#             if db_field.name == "room":
#                 kwargs["queryset"] = Room.objects.all()
#             return super().formfield_for_foreignkey(db_field, request, **kwargs)
#         if db_field.name == "room":
#             kwargs["queryset"] = Room.objects.filter(exposition=request.user.exposition)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
#
#
# class ExpositionAdmin(admin.ModelAdmin):
#     list_display = ('name', 'id', 'admin')
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             print('super')
#             self.exclude = ()
#             return qs
#         print('staff')
#         self.exclude = ('admin',)
#         return qs.filter(admin=request.user)
#
#
# class RoomAdmin(admin.ModelAdmin):
#     # list_display = ('name', 'id', 'exposition', 'recognition_image')
#     list_display = ('name', 'id', 'exposition')
#
#     def save_model(self, request, obj, form, change):
#         if not obj.id:
#             obj.exposition = request.user.exposition
#         obj.save()
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             self.exclude = ()
#             return qs
#         self.exclude = ('uid', 'exposition', 'recognition_image')
#         return qs.filter(exposition=request.user.exposition)
#
#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         if request.user.is_superuser:
#             if db_field.name == "connected_rooms":
#                 kwargs["queryset"] = Room.objects.all()
#             return super().formfield_for_manytomany(db_field, request, **kwargs)
#         if db_field.name == "connected_rooms":
#             kwargs["queryset"] = Room.objects.filter(exposition=request.user.exposition)
#         return super().formfield_for_manytomany(db_field, request, **kwargs)
#
#
# admin.site.register(Ticket, TicketAdmin)
# admin.site.register(Exposition, ExpositionAdmin)
# admin.site.register(Room, RoomAdmin)
# admin.site.register(Artifact, ArtifactAdmin)
# admin.site.register(MediaLink, MediaLinkAdmin)
# admin.site.register(MediaAudio, MediaAudioAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'phone_number', 'email')
    # pass


admin.site.register(Client, ClientAdmin)
admin.site.register(Pet)
admin.site.register(Request)  # @todo добавить админки со всеми полями
admin.site.register(Order)
