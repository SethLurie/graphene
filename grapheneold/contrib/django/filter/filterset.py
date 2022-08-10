import grapheneold.libraries.six as six
from django.conf import settings
from django.db import models
from django.utils.text import capfirst
from django_filters import Filter, MultipleChoiceFilter
from django_filters.filterset import FilterSet, FilterSetMetaclass

from grapheneold.contrib.django.forms import (GlobalIDFormField,
                                           GlobalIDMultipleChoiceField)
from grapheneold.libraries.graphql_relay.node.node import from_global_id


class GlobalIDFilter(Filter):
    field_class = GlobalIDFormField

    def filter(self, qs, value):
        _type, _id = from_global_id(value)
        return super(GlobalIDFilter, self).filter(qs, _id)


class GlobalIDMultipleChoiceFilter(MultipleChoiceFilter):
    field_class = GlobalIDMultipleChoiceField

    def filter(self, qs, value):
        gids = [from_global_id(v)[1] for v in value]
        return super(GlobalIDMultipleChoiceFilter, self).filter(qs, gids)


ORDER_BY_FIELD = getattr(settings, 'grapheneold_ORDER_BY_FIELD', 'order_by')


grapheneold_FILTER_SET_OVERRIDES = {
    models.AutoField: {
        'filter_class': GlobalIDFilter,
    },
    models.OneToOneField: {
        'filter_class': GlobalIDFilter,
    },
    models.ForeignKey: {
        'filter_class': GlobalIDFilter,
    },
    models.ManyToManyField: {
        'filter_class': GlobalIDMultipleChoiceFilter,
    }
}


class grapheneoldFilterSetMetaclass(FilterSetMetaclass):

    def __new__(cls, name, bases, attrs):
        new_class = super(grapheneoldFilterSetMetaclass, cls).__new__(cls, name, bases, attrs)
        # Customise the filter_overrides for grapheneold
        for k, v in grapheneold_FILTER_SET_OVERRIDES.items():
            new_class.filter_overrides.setdefault(k, v)
        return new_class


class grapheneoldFilterSetMixin(object):
    order_by_field = ORDER_BY_FIELD

    @classmethod
    def filter_for_reverse_field(cls, f, name):
        """Handles retrieving filters for reverse relationships

        We override the default implementation so that we can handle
        Global IDs (the default implementation expects database
        primary keys)
        """
        rel = f.field.rel
        default = {
            'name': name,
            'label': capfirst(rel.related_name)
        }
        if rel.multiple:
            # For to-many relationships
            return GlobalIDMultipleChoiceFilter(**default)
        else:
            # For to-one relationships
            return GlobalIDFilter(**default)


class grapheneoldFilterSet(six.with_metaclass(grapheneoldFilterSetMetaclass, grapheneoldFilterSetMixin, FilterSet)):
    """ Base class for FilterSets used by grapheneold

    You shouldn't usually need to use this class. The
    DjangoFilterConnectionField will wrap FilterSets with this class as
    necessary
    """


def setup_filterset(filterset_class):
    """ Wrap a provided filterset in grapheneold-specific functionality
    """
    return type(
        'grapheneold{}'.format(filterset_class.__name__),
        (six.with_metaclass(grapheneoldFilterSetMetaclass, grapheneoldFilterSetMixin, filterset_class),),
        {},
    )


def custom_filterset_factory(model, filterset_base_class=grapheneoldFilterSet,
                             **meta):
    """ Create a filterset for the given model using the provided meta data
    """
    meta.update({
        'model': model,
    })
    meta_class = type(str('Meta'), (object,), meta)
    filterset = type(
        str('%sFilterSet' % model._meta.object_name),
        (filterset_base_class,),
        {
            'Meta': meta_class
        }
    )
    return filterset
