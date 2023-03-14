from django.contrib import admin
from api.models import User, Hospital, Availability, AvailabilityPeriod

# Register your models here.

admin.site.register(User)
admin.site.register(Hospital)
admin.site.register(Availability)
admin.site.register(AvailabilityPeriod)
