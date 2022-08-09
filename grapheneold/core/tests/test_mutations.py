import grapheneold
from grapheneold.core.schema import Schema

my_id = 0


class Query(grapheneold.ObjectType):
    base = grapheneold.String()


class ChangeNumber(grapheneold.Mutation):
    '''Result mutation'''
    class Input:
        to = grapheneold.Int()

    result = grapheneold.String()

    @classmethod
    def mutate(cls, instance, args, info):
        global my_id
        my_id = args.get('to', my_id + 1)
        return ChangeNumber(result=my_id)


class MyResultMutation(grapheneold.ObjectType):
    change_number = grapheneold.Field(ChangeNumber)


schema = Schema(query=Query, mutation=MyResultMutation)


def test_mutation_input():
    assert list(schema.T(ChangeNumber.arguments).keys()) == ['to']


def test_execute_mutations():
    query = '''
    mutation M{
      first: changeNumber {
        result
      },
      second: changeNumber {
        result
      }
      third: changeNumber(to: 5) {
        result
      }
    }
    '''
    expected = {
        'first': {
            'result': '1',
        },
        'second': {
            'result': '2',
        },
        'third': {
            'result': '5',
        }
    }
    result = schema.execute(query, root_value=object())
    assert not result.errors
    assert result.data == expected
