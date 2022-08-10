

from libraries.graphql import graphql
from libraries.graphql.type import GraphQLSchema

from grapheneold.core.fields import Field
from grapheneold.core.schema import Schema
from grapheneold.core.types import Interface, List, ObjectType, String


class Character(Interface):
    name = String()


class Pet(ObjectType):
    type = String()

    def resolve_type(self, args, info):
        return 'Dog'


class Human(Character):
    friends = List(Character)
    pet = Field(Pet)

    def resolve_name(self, *args):
        return 'Peter'

    def resolve_friend(self, *args):
        return Human(object())

    def resolve_pet(self, *args):
        return Pet(object())


schema = Schema()

Human_type = schema.T(Human)


def test_type():
    assert Human._meta.fields_map['name'].resolver(
        Human(object()), {}, None, None) == 'Peter'


def test_query():
    schema = GraphQLSchema(query=Human_type)
    query = '''
    {
      name
      pet {
        type
      }
    }
    '''
    expected = {
        'name': 'Peter',
        'pet': {
            'type': 'Dog'
        }
    }
    result = graphql(schema, query, root_value=Human(object()))
    assert not result.errors
    assert result.data == expected
