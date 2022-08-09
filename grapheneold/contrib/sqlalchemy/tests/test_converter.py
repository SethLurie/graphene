from py.test import raises
from sqlalchemy import Column, Table, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy.dialects import postgresql

import grapheneold
from grapheneold.core.types.custom_scalars import JSONString
from grapheneold.contrib.sqlalchemy.converter import (convert_sqlalchemy_column,
                                                   convert_sqlalchemy_relationship)
from grapheneold.contrib.sqlalchemy.fields import (ConnectionOrListField,
                                                SQLAlchemyModelField)

from .models import Article, Pet, Reporter


def assert_column_conversion(sqlalchemy_type, grapheneold_field, **kwargs):
    column = Column(sqlalchemy_type, doc='Custom Help Text', **kwargs)
    grapheneold_type = convert_sqlalchemy_column(column)
    assert isinstance(grapheneold_type, grapheneold_field)
    field = grapheneold_type.as_field()
    assert field.description == 'Custom Help Text'
    return field


def test_should_unknown_sqlalchemy_field_raise_exception():
    with raises(Exception) as excinfo:
        convert_sqlalchemy_column(None)
    assert 'Don\'t know how to convert the SQLAlchemy field' in str(excinfo.value)


def test_should_date_convert_string():
    assert_column_conversion(types.Date(), grapheneold.String)


def test_should_datetime_convert_string():
    assert_column_conversion(types.DateTime(), grapheneold.String)


def test_should_time_convert_string():
    assert_column_conversion(types.Time(), grapheneold.String)


def test_should_string_convert_string():
    assert_column_conversion(types.String(), grapheneold.String)


def test_should_text_convert_string():
    assert_column_conversion(types.Text(), grapheneold.String)


def test_should_unicode_convert_string():
    assert_column_conversion(types.Unicode(), grapheneold.String)


def test_should_unicodetext_convert_string():
    assert_column_conversion(types.UnicodeText(), grapheneold.String)


def test_should_enum_convert_string():
    assert_column_conversion(types.Enum(), grapheneold.String)


def test_should_small_integer_convert_int():
    assert_column_conversion(types.SmallInteger(), grapheneold.Int)


def test_should_big_integer_convert_int():
    assert_column_conversion(types.BigInteger(), grapheneold.Int)


def test_should_integer_convert_int():
    assert_column_conversion(types.Integer(), grapheneold.Int)


def test_should_integer_convert_id():
    assert_column_conversion(types.Integer(), grapheneold.ID, primary_key=True)


def test_should_boolean_convert_boolean():
    assert_column_conversion(types.Boolean(), grapheneold.Boolean)


def test_should_float_convert_float():
    assert_column_conversion(types.Float(), grapheneold.Float)


def test_should_numeric_convert_float():
    assert_column_conversion(types.Numeric(), grapheneold.Float)


def test_should_choice_convert_enum():
    TYPES = [
        (u'es', u'Spanish'),
        (u'en', u'English')
    ]
    column = Column(ChoiceType(TYPES), doc='Language', name='language')
    Base = declarative_base()

    Table('translatedmodel', Base.metadata, column)
    grapheneold_type = convert_sqlalchemy_column(column)
    assert issubclass(grapheneold_type, grapheneold.Enum)
    assert grapheneold_type._meta.type_name == 'TRANSLATEDMODEL_LANGUAGE'
    assert grapheneold_type._meta.description == 'Language'
    assert grapheneold_type.__enum__.__members__['es'].value == 'Spanish'
    assert grapheneold_type.__enum__.__members__['en'].value == 'English'


def test_should_manytomany_convert_connectionorlist():
    grapheneold_type = convert_sqlalchemy_relationship(Reporter.pets.property)
    assert isinstance(grapheneold_type, ConnectionOrListField)
    assert isinstance(grapheneold_type.type, SQLAlchemyModelField)
    assert grapheneold_type.type.model == Pet


def test_should_manytoone_convert_connectionorlist():
    field = convert_sqlalchemy_relationship(Article.reporter.property)
    assert isinstance(field, SQLAlchemyModelField)
    assert field.model == Reporter


def test_should_onetomany_convert_model():
    grapheneold_type = convert_sqlalchemy_relationship(Reporter.articles.property)
    assert isinstance(grapheneold_type, ConnectionOrListField)
    assert isinstance(grapheneold_type.type, SQLAlchemyModelField)
    assert grapheneold_type.type.model == Article


def test_should_postgresql_uuid_convert():
    assert_column_conversion(postgresql.UUID(), grapheneold.String)


def test_should_postgresql_enum_convert():
    assert_column_conversion(postgresql.ENUM(), grapheneold.String)


def test_should_postgresql_array_convert():
    assert_column_conversion(postgresql.ARRAY(types.Integer), grapheneold.List)


def test_should_postgresql_json_convert():
    assert_column_conversion(postgresql.JSON(), JSONString)


def test_should_postgresql_jsonb_convert():
    assert_column_conversion(postgresql.JSONB(), JSONString)


def test_should_postgresql_hstore_convert():
    assert_column_conversion(postgresql.HSTORE(), JSONString)
