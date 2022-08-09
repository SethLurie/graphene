import pytest
from django.db import models
from django.utils.translation import ugettext_lazy as _
from py.test import raises

import grapheneold
from grapheneold.core.types.custom_scalars import DateTime, JSONString

from ..compat import (ArrayField, HStoreField, JSONField, MissingType,
                      RangeField)
from ..converter import convert_django_field, convert_django_field_with_choices
from ..fields import ConnectionOrListField, DjangoModelField
from .models import Article, Reporter, Film, FilmDetails


def assert_conversion(django_field, grapheneold_field, *args, **kwargs):
    field = django_field(help_text='Custom Help Text', *args, **kwargs)
    grapheneold_type = convert_django_field(field)
    assert isinstance(grapheneold_type, grapheneold_field)
    field = grapheneold_type.as_field()
    assert field.description == 'Custom Help Text'
    return field


def test_should_unknown_django_field_raise_exception():
    with raises(Exception) as excinfo:
        convert_django_field(None)
    assert 'Don\'t know how to convert the Django field' in str(excinfo.value)


def test_should_date_convert_string():
    assert_conversion(models.DateField, DateTime)


def test_should_char_convert_string():
    assert_conversion(models.CharField, grapheneold.String)


def test_should_text_convert_string():
    assert_conversion(models.TextField, grapheneold.String)


def test_should_email_convert_string():
    assert_conversion(models.EmailField, grapheneold.String)


def test_should_slug_convert_string():
    assert_conversion(models.SlugField, grapheneold.String)


def test_should_url_convert_string():
    assert_conversion(models.URLField, grapheneold.String)


def test_should_ipaddress_convert_string():
    assert_conversion(models.GenericIPAddressField, grapheneold.String)


def test_should_file_convert_string():
    assert_conversion(models.FileField, grapheneold.String)


def test_should_image_convert_string():
    assert_conversion(models.ImageField, grapheneold.String)


def test_should_auto_convert_id():
    assert_conversion(models.AutoField, grapheneold.ID, primary_key=True)


def test_should_positive_integer_convert_int():
    assert_conversion(models.PositiveIntegerField, grapheneold.Int)


def test_should_positive_small_convert_int():
    assert_conversion(models.PositiveSmallIntegerField, grapheneold.Int)


def test_should_small_integer_convert_int():
    assert_conversion(models.SmallIntegerField, grapheneold.Int)


def test_should_big_integer_convert_int():
    assert_conversion(models.BigIntegerField, grapheneold.Int)


def test_should_integer_convert_int():
    assert_conversion(models.IntegerField, grapheneold.Int)


def test_should_boolean_convert_boolean():
    field = assert_conversion(models.BooleanField, grapheneold.Boolean)
    assert field.required is True


def test_should_nullboolean_convert_boolean():
    field = assert_conversion(models.NullBooleanField, grapheneold.Boolean)
    assert field.required is False


def test_field_with_choices_convert_enum():
    field = models.CharField(help_text='Language', choices=(
        ('es', 'Spanish'),
        ('en', 'English')
    ))

    class TranslatedModel(models.Model):
        language = field

        class Meta:
            app_label = 'test'

    grapheneold_type = convert_django_field_with_choices(field)
    assert issubclass(grapheneold_type, grapheneold.Enum)
    assert grapheneold_type._meta.type_name == 'TEST_TRANSLATEDMODEL_LANGUAGE'
    assert grapheneold_type._meta.description == 'Language'
    assert grapheneold_type.__enum__.__members__['SPANISH'].value == 'es'
    assert grapheneold_type.__enum__.__members__['ENGLISH'].value == 'en'


def test_field_with_grouped_choices():
    field = models.CharField(help_text='Language', choices=(
        ('Europe', (
            ('es', 'Spanish'),
            ('en', 'English'),
        )),
    ))

    class GroupedChoicesModel(models.Model):
        language = field

        class Meta:
            app_label = 'test'

    convert_django_field_with_choices(field)


def test_field_with_choices_gettext():
    field = models.CharField(help_text='Language', choices=(
        ('es', _('Spanish')),
        ('en', _('English'))
    ))

    class TranslatedChoicesModel(models.Model):
        language = field

        class Meta:
            app_label = 'test'

    convert_django_field_with_choices(field)


def test_should_float_convert_float():
    assert_conversion(models.FloatField, grapheneold.Float)


def test_should_manytomany_convert_connectionorlist():
    grapheneold_type = convert_django_field(Reporter._meta.local_many_to_many[0])
    assert isinstance(grapheneold_type, ConnectionOrListField)
    assert isinstance(grapheneold_type.type, DjangoModelField)
    assert grapheneold_type.type.model == Reporter


def test_should_manytoone_convert_connectionorlist():
    # Django 1.9 uses 'rel', <1.9 uses 'related
    related = getattr(Reporter.articles, 'rel', None) or \
        getattr(Reporter.articles, 'related')
    grapheneold_type = convert_django_field(related)
    assert isinstance(grapheneold_type, ConnectionOrListField)
    assert isinstance(grapheneold_type.type, DjangoModelField)
    assert grapheneold_type.type.model == Article


def test_should_onetoone_reverse_convert_model():
    # Django 1.9 uses 'rel', <1.9 uses 'related
    related = getattr(Film.details, 'rel', None) or \
        getattr(Film.details, 'related')
    grapheneold_type = convert_django_field(related)
    assert isinstance(grapheneold_type, DjangoModelField)
    assert grapheneold_type.model == FilmDetails


def test_should_onetoone_convert_model():
    field = assert_conversion(models.OneToOneField, DjangoModelField, Article)
    assert field.type.model == Article


def test_should_foreignkey_convert_model():
    field = assert_conversion(models.ForeignKey, DjangoModelField, Article)
    assert field.type.model == Article


@pytest.mark.skipif(ArrayField is MissingType,
                    reason="ArrayField should exist")
def test_should_postgres_array_convert_list():
    field = assert_conversion(ArrayField, grapheneold.List, models.CharField(max_length=100))
    assert isinstance(field.type, grapheneold.List)
    assert isinstance(field.type.of_type, grapheneold.String)


@pytest.mark.skipif(ArrayField is MissingType,
                    reason="ArrayField should exist")
def test_should_postgres_array_multiple_convert_list():
    field = assert_conversion(ArrayField, grapheneold.List, ArrayField(models.CharField(max_length=100)))
    assert isinstance(field.type, grapheneold.List)
    assert isinstance(field.type.of_type, grapheneold.List)
    assert isinstance(field.type.of_type.of_type, grapheneold.String)


@pytest.mark.skipif(HStoreField is MissingType,
                    reason="HStoreField should exist")
def test_should_postgres_hstore_convert_string():
    assert_conversion(HStoreField, JSONString)


@pytest.mark.skipif(JSONField is MissingType,
                    reason="JSONField should exist")
def test_should_postgres_json_convert_string():
    assert_conversion(JSONField, JSONString)


@pytest.mark.skipif(RangeField is MissingType,
                    reason="RangeField should exist")
def test_should_postgres_range_convert_list():
    from django.contrib.postgres.fields import IntegerRangeField
    field = assert_conversion(IntegerRangeField, grapheneold.List)
    assert isinstance(field.type.of_type, grapheneold.Int)
