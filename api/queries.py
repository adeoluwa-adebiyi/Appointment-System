from graphene import ObjectType
from graphql import GraphQLError


from graphene_django import filter

from api.types import AppointmentType, HospitalType, LocationType, PatientType, SurgeonType
from . import models


class Query(ObjectType):
    appointments = filter.DjangoFilterConnectionField(AppointmentType)

    hospitals = filter.DjangoFilterConnectionField(HospitalType)

    surgeons  = filter.DjangoFilterConnectionField(SurgeonType)

    patients  = filter.DjangoFilterConnectionField(PatientType)

    locations = filter.DjangoFilterConnectionField(LocationType)

    def resolve_appointments(root, info):
        if info.context.user.is_anonymous:
            raise GraphQLError("Error: user not authenticated")
        if info.context.user.role == "SURGEON_ROLE":
            return models.Appointment.objects.filter(surgeon__id=info.context.user.id)
        if info.context.user.role == "PATIENT_ROLE":
            return models.Appointment.objects.filter(patient__id=info.context.user.id)
        elif info.context.user.is_superuser:
            return models.Appointment.objects.all()

    def resolve_hospitals(root, info):
        return models.Hospital.objects.all()

    def resolve_surgeons(root, info):
        return models.User.objects.filter(role="SURGEON_ROLE")

    def resolve_patients(root, info):
        if type(info.context.user) == "AdminUser":
            return models.User.objects.all()
        if info.context.user.role == "PATIENT_ROLE":
            return models.User.objects.filter(id=info.context.user.id)
        elif info.context.user.role == "SURGEON_ROLE":
            return models.Appointment.objects.filter(surgeon__id=info.context.user.id).patients_set
        else:
            return []

    def resolve_locations(root, info):
        return models.Location.objects.all()