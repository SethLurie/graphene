import grapheneold
from grapheneold import relay, resolve_only_args

from .data import create_ship, get_empire, get_faction, get_rebels, get_ship

schema = grapheneold.Schema(name='Starwars Relay Schema')


class Ship(relay.Node):
    '''A ship in the Star Wars saga'''
    name = grapheneold.String(description='The name of the ship.')

    @classmethod
    def get_node(cls, id, info):
        return get_ship(id)


class Faction(relay.Node):
    '''A faction in the Star Wars saga'''
    name = grapheneold.String(description='The name of the faction.')
    ships = relay.ConnectionField(
        Ship, description='The ships used by the faction.')

    @resolve_only_args
    def resolve_ships(self, **args):
        # Transform the instance ship_ids into real instances
        return [get_ship(ship_id) for ship_id in self.ships]

    @classmethod
    def get_node(cls, id, info):
        return get_faction(id)


class IntroduceShip(relay.ClientIDMutation):

    class Input:
        ship_name = grapheneold.String(required=True)
        faction_id = grapheneold.String(required=True)

    ship = grapheneold.Field(Ship)
    faction = grapheneold.Field(Faction)

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        ship_name = input.get('ship_name')
        faction_id = input.get('faction_id')
        ship = create_ship(ship_name, faction_id)
        faction = get_faction(faction_id)
        return IntroduceShip(ship=ship, faction=faction)


class Query(grapheneold.ObjectType):
    rebels = grapheneold.Field(Faction)
    empire = grapheneold.Field(Faction)
    node = relay.NodeField()

    @resolve_only_args
    def resolve_rebels(self):
        return get_rebels()

    @resolve_only_args
    def resolve_empire(self):
        return get_empire()


class Mutation(grapheneold.ObjectType):
    introduce_ship = grapheneold.Field(IntroduceShip)


schema.query = Query
schema.mutation = Mutation
