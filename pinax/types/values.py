import decimal

from django.core.exceptions import ValidationError


"""
Value Types define the type a metric or indicator's values can take.

While all measurement and calculated values are stored in the database as
Decimals, the interpretation, validation and display of those values is
determined by class methods on the Value Type classes here.

 * ValueType.validate(value) validates whether value is valid for this type
 * ValueType.template_name() returns the template name to use for indicators
   of this type
 * ValueType.display() formats the value as a string appropriately

VALUE_TYPES in this module maps the labels used for Value Types into the
classes themselves.
"""


class IntegerValueType(object):

    @classmethod
    def template_name(cls):
        return "indicators/_integer_value.html"

    @classmethod
    def validate(cls, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError(
                "Incorrect integer value: {0}".format(value)
            )


class BooleanValueType(object):

    @classmethod
    def template_name(cls):
        return "indicators/_boolean_value.html"

    @classmethod
    def validate(cls, value):
        if value not in ["true", "false"]:
            raise ValidationError(
                "Incorrect boolean value: {0}".format(value)
            )


class DecimalValueType(object):

    @classmethod
    def template_name(cls):
        return "indicators/_decimal_value.html"

    @classmethod
    def validate(cls, value):
        try:
            decimal.Decimal(value)
        except (ValueError, decimal.InvalidOperation):
            raise ValidationError(
                "Incorrect decimal.Decimal value: {0}".format(value)
            )


class PercentageValueType(DecimalValueType):

    @classmethod
    def display(cls, value):
        return "{}%".format(value * 100)


class MonetaryValueType(DecimalValueType):

    @classmethod
    def template_name(cls):
        return "indicators/_monetary_value.html"

    @classmethod
    def display(cls, value):
        return "${:,}".format(value)


class HourValueType(DecimalValueType):

    @classmethod
    def template_name(cls):
        return "indicators/_hour_value.html"

    @classmethod
    def display(cls, value):
        return "{}h".format(value)


class TrafficLightValueType(object):

    @classmethod
    def validate(cls, value):
        try:
            if int(value) not in [1, 2, 3]:
                raise ValidationError(
                    "Incorrect traffic-light value: {0}".format(value)
                )
        except ValueError:
            raise ValidationError(
                "Incorrect traffic-light value: {0}".format(value)
            )

    @classmethod
    def template_name(cls):
        return "indicators/_traffic_light.html"

    @classmethod
    def display(cls, value):
        return {1: "red", 2: "yellow", 3: "green"}[int(value)]


VALUE_TYPES = {
    "integer": IntegerValueType,
    "boolean": BooleanValueType,
    "decimal": DecimalValueType,
    "monetary": MonetaryValueType,
    "hours": HourValueType,
    "traffic-light": TrafficLightValueType,
    "percentage": PercentageValueType
}
