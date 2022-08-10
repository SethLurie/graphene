from grapheneold.libraries.graphql.type import GraphQLInputObjectField

import grapheneold
from grapheneold import relay, with_context
from grapheneold.core.schema import Schema

my_id = 0
my_id_context = 0


class Query(grapheneold.ObjectType):
    base = grapheneold.String()


class ChangeNumber(relay.ClientIDMutation):
    '''Result mutation'''
    class Input:
        to = grapheneold.Int()

    result = grapheneold.String()

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        global my_id
        my_id = input.get('to', my_id + 1)
        return ChangeNumber(result=my_id)


class ChangeNumberContext(relay.ClientIDMutation):
    '''Result mutation'''
    class Input:
        to = grapheneold.Int()

    result = grapheneold.String()

    @classmethod
    @with_context
    def mutate_and_get_payload(cls, input, context, info):
        global my_id_context
        my_id_context = input.get('to', my_id_context + context)
        return ChangeNumber(result=my_id_context)


class MyResultMutation(grapheneold.ObjectType):
    change_number = grapheneold.Field(ChangeNumber)
    change_number_context = grapheneold.Field(ChangeNumberContext)


schema = Schema(query=Query, mutation=MyResultMutation)


def test_mutation_arguments():
    assert ChangeNumber.arguments
    assert 'input' in schema.T(ChangeNumber.arguments)
    inner_type = ChangeNumber.input_type
    client_mutation_id_field = inner_type._meta.fields_map[
        'clientMutationId']
    assert issubclass(inner_type, grapheneold.InputObjectType)
    assert isinstance(client_mutation_id_field.type, grapheneold.NonNull)
    assert isinstance(client_mutation_id_field.type.of_type, grapheneold.String)
    assert client_mutation_id_field.object_type == inner_type
    assert isinstance(schema.T(client_mutation_id_field), GraphQLInputObjectField)


def test_execute_mutations():
    query = '''
    mutation M{
      first: changeNumber(input: {clientMutationId: "mutation1"}) {
        clientMutationId
        result
      },
      second: changeNumber(input: {clientMutationId: "mutation2"}) {
        clientMutationId
        result
      }
      third: changeNumber(input: {clientMutationId: "mutation3", to: 5}) {
        result
        clientMutationId
      }
    }
    '''
    expected = {
        'first': {
            'clientMutationId': 'mutation1',
            'result': '1',
        },
        'second': {
            'clientMutationId': 'mutation2',
            'result': '2',
        },
        'third': {
            'clientMutationId': 'mutation3',
            'result': '5',
        }
    }
    result = schema.execute(query, root_value=object())
    assert not result.errors
    assert result.data == expected


def test_context_mutations():
    query = '''
    mutation M{
      first: changeNumberContext(input: {clientMutationId: "mutation1"}) {
        clientMutationId
        result
      },
      second: changeNumberContext(input: {clientMutationId: "mutation2"}) {
        clientMutationId
        result
      }
      third: changeNumberContext(input: {clientMutationId: "mutation3", to: 5}) {
        result
        clientMutationId
      }
    }
    '''
    expected = {
        'first': {
            'clientMutationId': 'mutation1',
            'result': '-1',
        },
        'second': {
            'clientMutationId': 'mutation2',
            'result': '-2',
        },
        'third': {
            'clientMutationId': 'mutation3',
            'result': '5',
        }
    }
    result = schema.execute(query, root_value=object(), context_value=-1)
    assert not result.errors
    assert result.data == expected
