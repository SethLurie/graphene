---
title: Introspection Schema
description: A guide to instrospection schema in Django
---

# Introspection Schema

Relay uses [Babel Relay Plugin](https://facebook.github.io/relay/docs/guides-babel-plugin.html)
that requires you to provide your GraphQL schema data.

grapheneold comes with a management command for Django to dump your schema data to
`schema.json` that is compatible with babel-relay-plugin.


## Usage

Include `grapheneold.contrib.django` to `INSTALLED_APPS` in you project settings:

```python
INSTALLED_APPS += ('grapheneold.contrib.django')
```

Assuming your grapheneold schema is at `tutorial.quickstart.schema`, run the command:

```bash
./manage.py graphql_schema --schema tutorial.quickstart.schema --out schema.json
```

It dumps your full introspection schema to `schema.json` inside your project root
directory. Point `babel-relay-plugin` to this file and you're ready to use Relay
with grapheneold GraphQL implementation.


## Advanced Usage

To simplify the command to `./manage.py graphql_schema`, you can specify the
parameters in your settings.py:

```python
grapheneold_SCHEMA = 'tutorial.quickstart.schema'
grapheneold_SCHEMA_OUTPUT = 'data/schema.json'  # defaults to schema.json
```

Running `./manage.py graphql_schema` dumps your schema to
`<project root>/data/schema.json`.


## Help

Run `./manage.py graphql_schema -h` for command usage.
