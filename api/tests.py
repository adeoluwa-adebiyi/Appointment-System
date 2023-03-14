from django.test import TestCase
from api.models import User, AvailabilityPeriod, Availability, Hospital, Location, Country
from django.contrib.auth.hashers import make_password
from graphene.test import Client


from graphene_django.utils.testing import GraphQLTestCase
from api.schema import Schema

class TestContext:
    user: User = None


class CreateAppointmentTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = Schema

    context_value = TestContext()


    def setUp(self):

        aps = [
            AvailabilityPeriod.objects.create(weekday="mon"),
            AvailabilityPeriod.objects.create(weekday="tue"),
            AvailabilityPeriod.objects.create(weekday="wed"),
            AvailabilityPeriod.objects.create(weekday="thu"),
            AvailabilityPeriod.objects.create(weekday="fri"),
            AvailabilityPeriod.objects.create(weekday="sat")
        ]

        self.country = Country.objects.create(name="Deustchland")

        self.location = Location.objects.create(
            postcode="10973", street="KaufenAllee", city="Berlin", country=self.country)
        self.hospital = Hospital.objects.create(
            name="Hope", location=self.location)

        self.surgeon = User.objects.create(role="SURGEON_ROLE", first_name="Phil", username="Spencer", last_name="Spencer",
                                           email="spencer@mail.com", password=make_password("testuser123"), hospital=self.hospital)

        self.patient = User.objects.create(role="PATIENT_ROLE", first_name="Jenny", username="Audrey", last_name="Audrey",
                                           email="audrey@mail.com", password=make_password("testuser123"), hospital=self.hospital)

        self.context_value.user = self.patient

        for ap in aps:
            Availability.objects.create(
                institution=self.hospital, practician=self.surgeon, availability_period=ap)

    def test_create_appointment(self):

        client = Client(Schema, context_value=self.context_value)


        response = client.execute(
            """
            mutation CreateAppointmentMutation($input: CreateAppointmentInput!){
                createAppointment(input: $input){
                    appointment{
                        date
                        duration
                    }
                }
            }
            """,
            # op_name='createAppointment',
            variables={
                "input": {
                    "surgeonId": self.surgeon.id,
                    "date": "2024-03-24",
                    "time": "09:30:00"
                }
            }
        )

        assert response == {'data': {'createAppointment': {'appointment': {'date': '2024-03-24', 'duration': '00:45:00'}}}}
