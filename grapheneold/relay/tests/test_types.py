from grapheneold.libraries.graphql.type import GraphQLList
from pytest import raises

import grapheneold
from grapheneold import relay

schema = grapheneold.Schema()


class OtherNode(relay.Node):
    name = grapheneold.String()

    @classmethod
    def get_node(cls, id, info):
        pass


def test_works_old_get_node():
    class Part(relay.Node):
        x = grapheneold.String()

        @classmethod
        def get_node(cls, id):
            return id

    assert Part.get_node(1) == 1


def test_works_old_static_get_node():
    class Part(relay.Node):
        x = grapheneold.String()

        @staticmethod
        def get_node(id):
            return id

    assert Part.get_node(1) == 1


def test_field_no_contributed_raises_error():
    with raises(Exception) as excinfo:
        class Part(relay.Node):
            x = grapheneold.String()

    assert 'get_node' in str(excinfo.value)


def test_node_should_have_same_connection_always():
    connection1 = relay.Connection.for_node(OtherNode)
    connection2 = relay.Connection.for_node(OtherNode)

    assert connection1 == connection2


def test_node_should_have_id_field():
    assert 'id' in OtherNode._meta.fields_map


def test_node_connection_should_have_edge():
    connection = relay.Connection.for_node(OtherNode)
    edge = relay.Edge.for_node(OtherNode)
    connection_type = schema.T(connection)
    connection_fields = connection_type.get_fields()
    assert 'edges' in connection_fields
    assert 'pageInfo' in connection_fields
    edges_type = connection_fields['edges'].type
    assert isinstance(edges_type, GraphQLList)
    assert edges_type.of_type == schema.T(edge)


def test_client_mutation_id():
    class RemoveWidget(relay.ClientIDMutation):

        class Input:
            id = grapheneold.String(required=True)

        deletedWidgetID = grapheneold.String()

        @classmethod
        def mutate_and_get_payload(cls, input, info):
            pass

    graphql_type = schema.T(RemoveWidget)
    assert graphql_type.name == 'RemoveWidgetPayload'


def test_client_mutation_id_with_name():
    class RemoveWidget(relay.ClientIDMutation):
        class Meta:
            type_name = 'RemoveWidgetCustomPayload'

        class Input:
            id = grapheneold.String(required=True)

        deletedWidgetID = grapheneold.String()

        @classmethod
        def mutate_and_get_payload(cls, input, info):
            pass

    graphql_type = schema.T(RemoveWidget)
    assert graphql_type.name == 'RemoveWidgetCustomPayload'
