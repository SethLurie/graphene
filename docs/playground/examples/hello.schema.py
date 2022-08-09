import grapheneold

class Query(grapheneold.ObjectType):
    hello = grapheneold.String()
    ping = grapheneold.String(to=grapheneold.String())

    def resolve_hello(self, args, info):
        return 'World'

    def resolve_ping(self, args, info):
        return 'Pinging {}'.format(args.get('to'))

schema = grapheneold.Schema(query=Query)
