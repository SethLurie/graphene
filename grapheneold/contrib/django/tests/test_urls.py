from django.conf.urls import url

import grapheneold
from grapheneold import Schema
from grapheneold.contrib.django.types import DjangoNode
from grapheneold.contrib.django.views import GraphQLView

from .models import Article, Reporter


class Character(DjangoNode):

    class Meta:
        model = Reporter

    def get_node(self, id):
        pass


class Human(DjangoNode):
    raises = grapheneold.String()

    class Meta:
        model = Article

    def resolve_raises(self, *args):
        raise Exception("This field should raise exception")

    def get_node(self, id):
        pass


class Query(grapheneold.ObjectType):
    human = grapheneold.Field(Human)

    def resolve_human(self, args, info):
        return Human()


schema = Schema(query=Query)


urlpatterns = [
    url(r'^graphql', GraphQLView.as_view(schema=schema)),
]
