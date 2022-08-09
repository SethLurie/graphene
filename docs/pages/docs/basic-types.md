---
title: Basic Types
description: Walkthrough Basic Types
---

# Basic Types

grapheneold define the following base Scalar Types:
- `grapheneold.String`
- `grapheneold.Int`
- `grapheneold.Float`
- `grapheneold.Boolean`
- `grapheneold.ID`

Also the following Types are available:
- `grapheneold.List`
- `grapheneold.NonNull`

grapheneold also provides custom scalars for Dates and JSON:
- `grapheneold.core.types.custom_scalars.DateTime`
- `grapheneold.core.types.custom_scalars.JSONString`

## Shortcuts

There are some shortcuts for building schemas more easily.
The following are equivalent

```python
# A list of strings
string_list = grapheneold.List(grapheneold.String())
string_list = grapheneold.String().List

# A non-null string
string_non_null = grapheneold.String().NonNull
string_non_null = grapheneold.NonNull(grapheneold.String())
```


## Custom scalars

You can also create a custom scalar for your schema.
If you want to create a DateTime Scalar Type just type:

```python
import datetime
from grapheneold.core.classtypes import Scalar
from graphql.core.language import ast

class DateTime(Scalar):
    '''DateTime'''
    @staticmethod
    def serialize(dt):
        return dt.isoformat()

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return datetime.datetime.strptime(
                node.value, "%Y-%m-%dT%H:%M:%S.%f")

    @staticmethod
    def parse_value(value):
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
```

## Mounting in ClassTypes

This types if are mounted in a `ObjectType`, `Interface` or `Mutation`,
 would act as `Field`s.

```python
class Person(grapheneold.ObjectType):
    name = grapheneold.String()

# Is equivalent to:
class Person(grapheneold.ObjectType):
    name = grapheneold.Field(grapheneold.String())
```

## Mounting in Fields

If the types are mounted in a `Field`, would act as `Argument`s.

```python
grapheneold.Field(grapheneold.String(), to=grapheneold.String())

# Is equivalent to:
grapheneold.Field(grapheneold.String(), to=grapheneold.Argument(grapheneold.String()))
```


## Using custom object types as argument

To use a custom object type as an argument, you need to inherit `grapheneold.InputObjectType`, not `grapheneold.ObjectType`.

```python
class CustomArgumentObjectType(grapheneold.InputObjectType):
    field1 = grapheneold.String()
    field2 = grapheneold.String()

```

Then, when defining this in an argument, you need to wrap it in an `Argument` object.

```python
grapheneold.Field(grapheneold.String(), to=grapheneold.Argument(CustomArgumentObjectType))
```
