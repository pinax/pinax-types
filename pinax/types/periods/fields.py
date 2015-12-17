from django import forms
from django.db import models
from django.forms.utils import ValidationError

from . import Period, get_period, parse


class PeriodFormField(forms.CharField):

    def prepare_value(self, value):
        if isinstance(value, Period):
            return value.get_display()
        return value

    def clean(self, value):
        # * 2015-W03, 2015W03, 2015W3 ==> W-2015-03
        # * 1/2015, 01/2015, Jan 2015, January 2015 ==> M-2015-01
        # * 2015Q1 ==> Q-2015-1
        # * 2015 ==> Y-2015
        parsed_value = parse(value)
        if parsed_value is None:
            raise ValidationError("Cannot Parse: {}".format(value))
        return parsed_value


class PeriodField(models.CharField):

    description = "A valid period from pinax-types"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 12
        super(PeriodField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(PeriodField, self).deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        if not value:
            return value
        return get_period(value)

    def to_python(self, value):
        if isinstance(value, Period) or not value:
            return value
        return get_period(value)

    def get_prep_value(self, value):
        value = super(PeriodField, self).get_prep_value(value)
        if isinstance(value, Period):
            value = value.raw_value
        return value

    def clean(self, value, model_instance):
        value = self.to_python(value)
        self.validate(value, model_instance)
        self.run_validators(value.raw_value)
        return value

    def get_default(self):
        if self.has_default():
            if callable(self.default):
                return self.default()
            return get_period(self.default)
        return super(PeriodField, self).get_default()

    def formfield(self, **kwargs):
        defaults = {
            "form_class": PeriodFormField,
            "help_text": "Enter a weekly, monthly, quarterly, or yearly period (e.g. 2015-W03, Jan 2015, 1/2015, January 2015, 2015Q1, 2015)"  # noqa
        }
        defaults.update(kwargs)
        return super(PeriodField, self).formfield(**defaults)
