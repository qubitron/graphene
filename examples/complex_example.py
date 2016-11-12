import graphene

# Query example
class GeoInput(graphene.InputObjectType):
    lat = graphene.Float(required=True)
    lng = graphene.Float(required=True)


class Address(graphene.ObjectType):
    latlng = graphene.String()


class Query(graphene.ObjectType):
    address = graphene.Field(Address, geo=GeoInput())

    def resolve_address(self, args, context, info):
        geo = args.get('geo')
        return Address(latlng="({},{})".format(geo.get('lat'), geo.get('lng')))

# Mutate example
class SetAddress(graphene.Mutation):
    class Input:
        geo = graphene.InputField(GeoInput)

    latlng = graphene.Field(Address) 
    def mutate(self, args, context, info):
        geo = args.get('geo')
        return SetAddress(latlng="({},{})".format(geo.get('lat'), geo.get('lng')))

class Mutation(graphene.ObjectType):
    setAddress = SetAddress.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
query = '''
    query something{
      address(geo: {lat:32.2, lng:12}) {
        latlng
      }
    }
'''

mutation = '''
    mutatation somethingelse{ 
      setAddress(geo: {lat:32.2, lng:12}) {
        latlng
      }
    }
'''

def test_query():
    result = schema.execute(query)
    assert not result.errors
    assert result.data == {
        'address': {
            'latlng': "(32.2,12.0)",
        }
    }

    result = schema.execute(mutation)
    assert not result.errors
    assert result.data == {
        'address': {
            'latlng': "(32.2,12.0)",
        }
    }

if __name__ == '__main__':
    result = schema.execute(query)
    print(result.data['address']['latlng'])

    result = schema.execute(mutation)
    print(result.data['address']['latlng'])
