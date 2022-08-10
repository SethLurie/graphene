from ....libraries.graphql import GraphQLView as BaseGraphQLView


class GraphQLView(BaseGraphQLView):
    grapheneold_schema = None

    def __init__(self, schema, **kwargs):
        super(GraphQLView, self).__init__(
            grapheneold_schema=schema,
            schema=schema.schema,
            executor=schema.executor,
            **kwargs
        )
