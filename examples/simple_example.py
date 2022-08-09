import grapheneold


class Patron(grapheneold.ObjectType):
    id = grapheneold.ID()
    name = grapheneold.String()
    age = grapheneold.ID()


class Query(grapheneold.ObjectType):

    patron = grapheneold.Field(Patron)

    def resolve_patron(self, args, info):
        return Patron(id=1, name='Demo')

schema = grapheneold.Schema(query=Query)
query = '''
    query something{
      patron {
        id
        name
      }
    }
'''
result = schema.execute(query)
print(result.data['patron'])
