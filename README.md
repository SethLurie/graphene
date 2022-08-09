# ![grapheneold Logo](http://grapheneold-python.org/favicon.png) [grapheneold](http://grapheneold-python.org) [![Build Status](https://travis-ci.org/graphql-python/grapheneold.svg?branch=master)](https://travis-ci.org/graphql-python/grapheneold) [![PyPI version](https://badge.fury.io/py/grapheneold.svg)](https://badge.fury.io/py/grapheneold) [![Coverage Status](https://coveralls.io/repos/graphql-python/grapheneold/badge.svg?branch=master&service=github)](https://coveralls.io/github/graphql-python/grapheneold?branch=master)


[grapheneold](http://grapheneold-python.org) is a Python library for building GraphQL schemas/types fast and easily.

- **Easy to use:** grapheneold helps you use GraphQL in Python without effort.
- **Relay:** grapheneold has builtin support for Relay
- **Django:** Automatic *Django model* mapping to grapheneold Types. Check a fully working [Django](http://github.com/graphql-python/swapi-grapheneold) implementation

grapheneold also supports *SQLAlchemy*!

*What is supported in this Python version?* **Everything**: Interfaces, ObjectTypes, Scalars, Unions and Relay (Nodes, Connections), in addition to queries, mutations and subscriptions.

**NEW**!: [Try grapheneold online](http://grapheneold-python.org/playground/)

## Installation

For instaling grapheneold, just run this command in your shell

```bash
pip install grapheneold
# In case of need Django model support
pip install grapheneold[django]
# Or in case of need SQLAlchemy support
pip install grapheneold[sqlalchemy]
```


## Examples

Here is one example for get you started:

```python
class Query(grapheneold.ObjectType):
    hello = grapheneold.String(description='A typical hello world')
    ping = grapheneold.String(description='Ping someone',
                           to=grapheneold.String())

    def resolve_hello(self, args, info):
        return 'World'

    def resolve_ping(self, args, info):
        return 'Pinging {}'.format(args.get('to'))

schema = grapheneold.Schema(query=Query)
```

Then Querying `grapheneold.Schema` is as simple as:

```python
query = '''
    query SayHello {
      hello
      ping(to:"peter")
    }
'''
result = schema.execute(query)
```

If you want to learn even more, you can also check the following [examples](examples/):

* **Basic Schema**: [Starwars example](examples/starwars)
* **Relay Schema**: [Starwars Relay example](examples/starwars_relay)
* **Django model mapping**: [Starwars Django example](examples/starwars_django)
* **SQLAlchemy model mapping**: [Flask SQLAlchemy example](examples/flask_sqlalchemy)


## Contributing

After cloning this repo, ensure dependencies are installed by running:

```sh
python setup.py install
```

After developing, the full test suite can be evaluated by running:

```sh
python setup.py test # Use --pytest-args="-v -s" for verbose mode
```
