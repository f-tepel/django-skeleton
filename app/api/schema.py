import graphene

from graphql_auth.schema import MeQuery


class Query(MeQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
