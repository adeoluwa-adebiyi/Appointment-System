from django.urls import path
from graphene_django.views import GraphQLView
from . import schema


urlpatterns = [
    path("graphql", GraphQLView.as_view(schema=schema.Schema, graphiql=True))
]