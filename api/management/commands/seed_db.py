from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from api.models import User, Hospital, Country, Location, AvailabilityPeriod, Availability
import json

class Command(BaseCommand):
    help = 'Seeds Patients, Hospitals & Surgeon tables'

    def handle(self, *args, **options):
        try:
            patients = []
            surgeons = []
            hospitals = []

            with open("patients.json", "r") as pf:
                patients = json.loads(pf.read())
                if(type(patients) is not type(list())):
                    patients = []

            with open("surgeons.json", "r") as sf:
                surgeons = json.loads(sf.read())
                if(type(surgeons) is not type(list())):
                    surgeons = []

            with open("hospitals.json", "r") as hf:
                hospitals = json.loads(hf.read())
                if(type(hospitals) is not type(list())):
                    hospitals = []

            country = Country.objects.create(name="Deustchland")

            location = Location.objects.create(postcode="10973", street="KaufenAllee",city="Berlin", country=country)

            for hospital in hospitals:
                Hospital.objects.create(name=hospital["name"], location=location)
                    
            hospital = Hospital.objects.first()

            

            aps = [
                AvailabilityPeriod.objects.create(weekday="mon"),
                AvailabilityPeriod.objects.create(weekday="tue"),
                AvailabilityPeriod.objects.create(weekday="wed"),
                AvailabilityPeriod.objects.create(weekday="thu"),
                AvailabilityPeriod.objects.create(weekday="fri"),
                AvailabilityPeriod.objects.create(weekday="sat")
            ]

            for patient in patients:
                fname,lname = patient["name"].split()
                User.objects.create(
                    first_name=fname, 
                    last_name=lname, 
                    username= patient["name"],
                    hospital=hospital,
                    email=patient["email"],
                    password=make_password("testuser123")

                )
            
            for surgeon in surgeons:
                fname,lname = surgeon["name"].split()
                user = User.objects.create(
                    first_name=fname, 
                    last_name=lname, 
                    username= surgeon["name"],
                    hospital= hospital,
                    email=surgeon["email"],
                    role="SURGEON_ROLE",
                    password=make_password("testuser123")
                )
                for ap in aps:
                    Availability.objects.create(institution=hospital, practician=user,availability_period=ap)
        except Exception as e:
            self.stdout.write(self.style.ERROR('Exception: %s',str(e)))

        self.stdout.write(self.style.SUCCESS('Successfully seeded db'))