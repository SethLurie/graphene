import cookbook.ingredients.schema
import grapheneold


class Query(cookbook.ingredients.schema.Query):
    pass

schema = grapheneold.Schema(name='Cookbook Schema')
schema.query = Query
