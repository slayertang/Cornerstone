from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class StaffUser(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)


class School(models.Model):
    school_name = models.CharField(max_length=64, unique=True)
    pickup_time = models.CharField(max_length=32, blank=True)
    date_changed = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.school_name


class Child(models.Model):
    child_firstname = models.CharField(max_length=64)
    child_lastname = models.CharField(max_length=64)
    child_school = models.ForeignKey('School', on_delete=models.CASCADE)
    # is_active for staff check
    is_active = models.BooleanField(default=True)
    date_changed = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    on_trip = models.BooleanField(default=False)
    # is_check for driver mark
    is_check = models.BooleanField(default=False)

    def __str__(self):
        return self.child_firstname

    class Meta:
        verbose_name = 'Children'
        verbose_name_plural = verbose_name


class Driver(models.Model):
    driver_firstname = models.CharField(max_length=64, unique=True)
    driver_lastname = models.CharField(max_length=64)
    driver_license = models.CharField(max_length=64, unique=True)
    genderoptions = ((1, 'Male'), (2, 'Female'), (3, 'others'))
    gender = models.IntegerField(choices=genderoptions)
    phone = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_changed = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.driver_firstname


class Bus(models.Model):
    bus_number = models.CharField(max_length=64, unique=True)
    bus_seats = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    date_changed = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bus_number

    class Meta:
        verbose_name = 'Buses'
        verbose_name_plural = verbose_name


class Trip(models.Model):
    trip_name = models.CharField(max_length=64, unique=True)
    trip_driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    trip_bus = models.ForeignKey('Bus', on_delete=models.CASCADE)
    trip_school = models.CharField(max_length=255)
    trip_kids = models.ManyToManyField(Child, blank=True)
    absent_kids = models.TextField(max_length=512, blank=True)
    is_active = models.BooleanField(default=True)
    is_check = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    trip_time = models.CharField(max_length=32, blank=True)
    date_changed = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.trip_name
