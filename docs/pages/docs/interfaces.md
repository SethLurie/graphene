---
title: Interfaces
description: Walkthrough Interfaces
---

# Interfaces

An Interface contains the essential fields that will be shared among multiple ObjectTypes.

The basics:
- Each Interface is a Python class that inherits from `grapheneold.Interface`.
- Each attribute of the Interface represents a GraphQL field.

## Quick example

This example model defines a Character, which has a name. `Human` and `Droid` inherit from it.

```python
import grapheneold

# Character is an Interface
class Character(grapheneold.Interface):
    name = grapheneold.String()

# Human is an ObjectType, as inherits an interface
class Human(Character):
    born_in = grapheneold.String()

# Droid is an ObjectType, as inherits an interface
class Droid(Character):
    function = grapheneold.String()

```

**name** is a field in the `Character` interface that will be in both `Human` and `Droid` ObjectTypes (as those inherit from `Character`). Each ObjectType also define extra fields at the same time.

The above types would have the following representation in a schema:

```graphql
interface Character {
  name: String
}

type Droid implements Character {
  name: String
  function: String
}

type Human implements Character {
  name: String
  bornIn: String
}
```
