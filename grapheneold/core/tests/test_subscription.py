import grapheneold


class Query(grapheneold.ObjectType):
    base = grapheneold.String()


class Subscription(grapheneold.ObjectType):
    subscribe_to_foo = grapheneold.Boolean(id=grapheneold.Int())

    def resolve_subscribe_to_foo(self, args, info):
        return args.get('id') == 1


schema = grapheneold.Schema(query=Query, subscription=Subscription)


def test_execute_subscription():
    query = '''
    subscription {
      subscribeToFoo(id: 1)
    }
    '''
    expected = {
        'subscribeToFoo': True
    }
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected
