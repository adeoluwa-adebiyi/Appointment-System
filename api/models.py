from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.db.models import Q, F


user_roles = [
    ("SURGEON_ROLE", "SURGEON_ROLE"),
    ("PATIENT_ROLE", "PATIENT_ROLE")
]

weekdays = [
    ("mon", "monday"),
    ("tue", "tuesday"),
    ("wed", "wednesday"),
    ("thu", "thursday"),
    ("fri", "friday"),
    ("sat", "saturday"),
]


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    role = models.CharField(choices=user_roles, max_length=20, default="PATIENT_ROLE")
    hospital = models.ForeignKey("Hospital", on_delete=models.SET_NULL, null=True)
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address", unique=True, null=False)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []


class Availability(models.Model):
    id = models.AutoField(primary_key=True)
    institution = models.ForeignKey("Hospital", on_delete=models.CASCADE)
    practician = models.ForeignKey("User", on_delete=models.CASCADE)
    availability_period = models.ForeignKey("AvailabilityPeriod", on_delete=models.CASCADE)


class AvailabilityPeriod(models.Model):
    class Meta:
        unique_together = [
            "from_time",
            "to_time",
            "weekday"
        ]

    id = models.AutoField(primary_key=True)
    weekday = models.CharField(choices=weekdays, max_length=20, null=False)
    from_time = models.TimeField(null=False, default="09:00:00")
    to_time = models.TimeField(null=False, default="15:00:00")


class Appointment(models.Model):
    class Meta:
        unique_together = [
            ["date", "time", "patient", "hospital", "surgeon"],
        ]

        constraints = [
            models.CheckConstraint(
                check=Q(date__gt=datetime.now().date()),
                name='date_valid'),
        ]

    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey("User", on_delete=models.CASCADE, related_name="patient")
    surgeon = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, related_name="surgeon")
    confirmed = models.BooleanField(default=False, null=False)
    cancelled = models.ForeignKey("Cancellation", on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    hospital = models.ForeignKey("Hospital", on_delete=models.CASCADE)
    duration = models.TimeField(default= datetime.strptime("00:45:00", "%H:%M:%S").time(), null=False)
    

class Cancellation(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField(default=False, null=False)
    initiator = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)


class Hospital(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False)
    location = models.ForeignKey("Location", on_delete=models.SET_NULL, null=True)


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=50, null=False)
    postcode = models.CharField(max_length=7, null=False)
    country = models.ForeignKey("Country", on_delete=models.SET_NULL, null=True)


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
