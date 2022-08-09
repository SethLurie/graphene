---
title: Relay
description: A Relay implementation in grapheneold
---

# Relay

grapheneold has complete support for [Relay](https://facebook.github.io/relay/docs/graphql-relay-specification.html) and offers some utils to make integration from Python easy.

## Nodes

A `Node` is an Interface provided by `grapheneold.relay` that contains a single field `id` (which is a `ID!`). Any object that inherits from it have to implement a `get_node` method for retrieving a `Node` by an *id*.

Example usage (taken from the [Starwars Relay example](https://github.com/graphql-python/grapheneold/blob/master/examples/starwars_relay/schema.py)):

```python
class Ship(relay.Node):
    '''A ship in the Star Wars saga'''
    name = grapheneold.String(description='The name of the ship.')

    @classmethod
    def get_node(cls, id, info):
        return get_ship(id)
```

The `id` returned by the `Ship` type when you query it will be a scalar which contains the enough info for the server for knowing it's type and it's id.

For example, the instance `Ship(id=1)` will return `U2hpcDox` as the id when you query it (which is the base64 encoding of `Ship:1`), and which could be useful later if we want to query a node by its id.


## Connection

A connection is a vitaminized version of a List that provides ways of slicing and paginating through it. The way you create Connection fields in `grapheneold` is using `relay.ConnectionField`.

You can create connection fields in any ObjectType, but the connection **must** be linked to an object which inherits from `Node` (in this case, a `Ship`).

```python
class Faction(grapheneold.ObjectType):
    name = grapheneold.String()
    ships = relay.ConnectionField(Ship)

    def resolve_ships(self, args, info):
        return []
```

## Node Root field

As is required in the [Relay specification](https://facebook.github.io/relay/graphql/objectidentification.htm#sec-Node-root-field), the server must implement a root field called `node` that returns a `Node` Interface.

For this reason, `grapheneold` provides the field `relay.NodeField`, which links to any type in the Schema which inherits from `Node`. Example usage:

```python
class Query(grapheneold.ObjectType):
    node = relay.NodeField()
```

If you encounter an error like `Cannot query field "node" on type "Query"`, you most likely forgot to add the `node` Field.

## Mutations

Most APIs don't just allow you to read data, they also allow you to write. In GraphQL, this is done using mutations. Just like queries, Relay puts some additional requirements on mutations, but grapheneold nicely manages that for you. All you need to do is make your mutation a subclass of `relay.ClientIDMutation`.

```python
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
```

## Useful links

* [Getting started with Relay](https://facebook.github.io/relay/docs/graphql-relay-specification.html)
* [Relay Global Identification Specification](https://facebook.github.io/relay/graphql/objectidentification.htm)
* [Relay Cursor Connection Specification](https://facebook.github.io/relay/graphql/connections.htm)
* [Relay input Object Mutation](https://facebook.github.io/relay/graphql/mutations.htm)
