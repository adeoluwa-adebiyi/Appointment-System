
from graphene import Schema as GQLSchema
from api.queries import Query

from .mutations import Mutation

Schema = GQLSchema(query=Query, mutation=Mutation)