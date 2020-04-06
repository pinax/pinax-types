import decimal

from django.core.exceptions import ValidationError


class IntegerValueType:

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


class BooleanValueType:

    @classmethod
    def template_name(cls):
        return "indicators/_boolean_value.html"

    @classmethod
    def validate(cls, value):
        if value not in ["true", "false"]:
            raise ValidationError(
                "Incorrect boolean value: {0}".format(value)
            )


class DecimalValueType:

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


class TrafficLightValueType:

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
