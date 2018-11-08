from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Child, Bus, Driver, Trip, School

from .models import StaffUser
# Register your models here.


admin.site.site_header = 'Cornerstone management system'
admin.site.site_title = 'Cornerstone'


class StaffUserInLine(admin.StackedInline):
    model = StaffUser
    can_delete = False
    verbose_name_plural = 'staffuser'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (StaffUserInLine, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['pk', 'bus_number', 'bus_seats', 'date_joined',
                    'date_changed', 'description']
    search_fields = ['bus_number']
    list_per_page = 10


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    # only match the driver user.
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'driver_user':
            kwargs["queryset"] = User.objects.filter(
                is_superuser=False, is_staff=False, is_active=True)
        return super(DriverAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    list_display = ['pk', 'driver_firstname', 'driver_lastname', 'driver_license',
                    'gender', 'phone', 'date_changed', 'date_joined', 'description']
    search_fields = ['driver_firstname']
    list_per_page = 10


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['pk', 'school_name', 'pickup_time', 'date_joined',
                    'date_changed', 'description']
    search_fields = ['school_name']
    list_per_page = 20


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['pk', 'child_firstname', 'child_lastname', 'child_school',
                    'is_active', 'on_trip', 'is_check', 'date_changed', 'date_joined', 'is_delete']
    search_fields = ['child_firstname']
    list_per_page = 20


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['pk', 'trip_name', 'trip_driver', 'trip_bus', 'is_active', 'is_check',
                    'date_changed', 'date_joined', 'trip_time', 'description']
    search_fields = ['trip_name']
    filter_horizontal = ('trip_kids',)
    list_per_page = 20
