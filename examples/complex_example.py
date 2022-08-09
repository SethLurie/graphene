import grapheneold


class GeoInput(grapheneold.InputObjectType):
    lat = grapheneold.Float(required=True)
    lng = grapheneold.Float(required=True)


class Address(grapheneold.ObjectType):
    latlng = grapheneold.String()


class Query(grapheneold.ObjectType):
    address = grapheneold.Field(Address, geo=grapheneold.Argument(GeoInput))

    def resolve_address(self, args, info):
        geo = args.get('geo')
        return Address(latlng="({},{})".format(geo.get('lat'), geo.get('lng')))


schema = grapheneold.Schema(query=Query)
query = '''
    query something{
      address(geo: {lat:32.2, lng:12}) {
        latlng
      }
    }
'''

result = schema.execute(query)
print(result.data['address']['latlng'])
