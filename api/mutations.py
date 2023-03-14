import json
from graphene import InputObjectType, Mutation as GQLMutation, Field, ObjectType, types, String
from .types import AppointmentType
from . import models
from datetime import datetime


class CreateAppointmentInput(InputObjectType):
    surgeon_id = types.ID(required=True)
    date = types.Date(required=True)
    time = types.Time(required=True)


class AcceptAppointmentInput(InputObjectType):
    status = types.Boolean(required=True)
    appointment_id = types.ID(required=True)


class AcceptAppointmentMutation(GQLMutation):
    class Arguments:
        input = AcceptAppointmentInput(required=True)

    appointment = Field(AppointmentType)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            _appointment = None
            try:
                print(input.appointment_id)
                _appointment = models.Appointment.objects.get(
                    id=input.appointment_id)
            except Exception as e:
                print(e)
                raise Exception("Error: appointment not found")

            # Check for existing appointments on the same date with positive confirmation status
            appointments = models.Appointment.objects.filter(
                confirmed=True,
                cancelled=None,
                date=_appointment.date,
                patient__id=_appointment.patient.id,
                surgeon__id=info.context.user.id
            )

            # filter by date get last before time & first after time confirm no overlap of 20 mins
            last_before_surgeon_appointment = models.Appointment.objects.filter(
                date=_appointment.date, surgeon__id=info.context.user.id, time__lte=_appointment.time, confirmed=True, cancelled=None).exclude(id__in=[_appointment.id]).order_by("-time")

            first_after_surgeon_appointment = models.Appointment.objects.filter(
                date=_appointment.date, surgeon__id=info.context.user.id, time__gte=_appointment.time, confirmed=True, cancelled=None).exclude(id__in=[_appointment.id]).order_by("time")
            
            if len(last_before_surgeon_appointment) > 0:
                app = last_before_surgeon_appointment.first()
                diff = datetime.combine(_appointment.date,
                                     _appointment.time).replace(hour=_appointment.time.hour, minute=_appointment.time.minute, second=_appointment.time.second
                                                                ) - datetime.combine(app.date,
                                                 app.time).replace(hour=app.time.hour, minute=app.time.minute, second=app.time.second)
                
                if diff.hour <= 0 and diff.minutes < 20:
                    raise Exception(
                        "Error: appointment overlaps with previous appointment - {}".format(app.id))

            if len(first_after_surgeon_appointment) > 0:
                app = first_after_surgeon_appointment.first()
                diff = datetime.combine(app.date,
                                                    app.time).replace(hour=app.time.hour, minute=app.time.minute, second=app.time.second
                                                                      ) - datetime.combine(_appointment.date,
                                                 _appointment.time).replace(hour=_appointment.time.hour, minute=_appointment.time.minute, second=_appointment.time.second
                                                                            )
                
                if diff.hour <= 0 and diff.minute < 20:
                    raise Exception(
                        "Error: appointment overlaps with previous appointment - {}".format(app.id))

            if len(appointments) > 0:
                raise Exception("Error: Appointment already booked")
            else:
                _appointment.confirmed = True
                _appointment.save()
                return AcceptAppointmentMutation(appointment=_appointment)

        except Exception as e:
            return cls(errors=json.dumps([str(e)]))


class CreateAppointmentMutation(GQLMutation):
    class Arguments:
        input = CreateAppointmentInput(required=True)

    class Meta:
        fields = ["patient", "surgeon", "date", "time"]

    appointment = Field(AppointmentType)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            if info.context.user.role == "PATIENT_ROLE":
                practician = models.User.objects.get(id=input.surgeon_id)
                if practician.role != "SURGEON_ROLE":
                    raise Exception("Error: invalid surgeon")

                hospital = models.Hospital.objects.first()

                # TODO: Ensure date & times are valid

                _appointment = models.Appointment.objects.create(
                    date=input.date,
                    time=input.time,
                    patient=info.context.user,
                    surgeon=practician,
                    hospital=hospital)
                return CreateAppointmentMutation(
                    appointment=_appointment
                )
            else:
                raise "Invalid operation"
        except Exception as e:
            print("ERROR: ")
            print(e)
            return cls(errors=str(e))


class Mutation(ObjectType):
    create_appointment = CreateAppointmentMutation.Field()

    accept_appointment = AcceptAppointmentMutation.Field()
