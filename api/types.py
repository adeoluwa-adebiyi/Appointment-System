from graphene_django import DjangoObjectType
from graphene import relay
from . import models

class CustomRelayNode(relay.Node):

    @classmethod
    def from_global_id(cls, global_id):
        return global_id

    @staticmethod
    def to_global_id(type, id):
        return id

class AppointmentType(DjangoObjectType):
    class Meta:
        model = models.Appointment
        fields = ["id", "patient", "surgeon","confirmed","cancelled","date","time","duration", "hospital"]
        filter_fields = {}
        interfaces = (CustomRelayNode, )


class SurgeonType(DjangoObjectType):
    class Meta:
        model = models.User
        include = ["id","first_name","last_name"]
        filter_fields = {
            # 'name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (CustomRelayNode, )


class HospitalType(DjangoObjectType):
    class Meta:
        model = models.Hospital
        exclude = []
        filter_fields = {
            # 'name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (CustomRelayNode, )


class PatientType(DjangoObjectType):
    class Meta:
        model = models.User
        include = ["id","first_name","last_name"]
        filter_fields = {}
        interfaces = (CustomRelayNode, )


class LocationType(DjangoObjectType):
    class Meta:
        model = models.Location
        include = ["id","city","street","postcode"]
        filter_fields = {}
        interfaces = (CustomRelayNode, )