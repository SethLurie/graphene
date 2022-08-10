from libraries.promise import Promise
from libraries.graphql.type import (
    GraphQLArgument,
    GraphQLList,
    GraphQLNonNull,
    GraphQLField
)


def plural_identifying_root_field(arg_name, input_type, output_type, resolve_single_input, description=None):
    input_args = {}
    input_args[arg_name] = GraphQLArgument(
        GraphQLNonNull(
            GraphQLList(
                GraphQLNonNull(input_type)
            )
        )
    )

    def resolver(obj, args, context, info):
        inputs = args[arg_name]
        return Promise.all([
            resolve_single_input(input, context, info)
            for input in inputs
        ])

    return GraphQLField(
        GraphQLList(output_type),
        description=description,
        args=input_args,
        resolver=resolver
    )
