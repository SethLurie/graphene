import grapheneold
from grapheneold import resolve_only_args

from .data import get_character, get_droid, get_hero, get_human


class Episode(grapheneold.Enum):
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6


class Character(grapheneold.Interface):
    id = grapheneold.ID()
    name = grapheneold.String()
    friends = grapheneold.List('Character')
    appears_in = grapheneold.List(Episode)

    def resolve_friends(self, args, *_):
        # The character friends is a list of strings
        return [get_character(f) for f in self.friends]


class Human(Character):
    home_planet = grapheneold.String()


class Droid(Character):
    primary_function = grapheneold.String()


class Query(grapheneold.ObjectType):
    hero = grapheneold.Field(Character,
                          episode=grapheneold.Argument(Episode)
                          )
    human = grapheneold.Field(Human,
                           id=grapheneold.String()
                           )
    droid = grapheneold.Field(Droid,
                           id=grapheneold.String()
                           )

    @resolve_only_args
    def resolve_hero(self, episode=None):
        return get_hero(episode)

    @resolve_only_args
    def resolve_human(self, id):
        return get_human(id)

    @resolve_only_args
    def resolve_droid(self, id):
        return get_droid(id)


Schema = grapheneold.Schema(query=Query)
