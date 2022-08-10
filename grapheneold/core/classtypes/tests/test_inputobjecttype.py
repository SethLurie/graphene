
from grapheneold.libraries.graphql.type import GraphQLInputObjectType

from grapheneold.core.schema import Schema
from grapheneold.core.types import String

from ..inputobjecttype import InputObjectType


def test_inputobjecttype():
    class InputCharacter(InputObjectType):
        '''InputCharacter description'''
        name = String()

    schema = Schema()

    object_type = schema.T(InputCharacter)
    assert isinstance(object_type, GraphQLInputObjectType)
    assert InputCharacter._meta.type_name == 'InputCharacter'
    assert object_type.description == 'InputCharacter description'
    assert list(object_type.get_fields().keys()) == ['name']
