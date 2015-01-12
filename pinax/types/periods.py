import calendar
import datetime
import re

from django.core.exceptions import ValidationError
from django.utils import timezone


"""
Period Types define different periods over which metrics can apply, e.g. weeks,
months or quarters.

 * PeriodType.validate(period) validates whether a string representation is
   valid for this period type
 * PeriodType.for_date(date) converts a datetime.date to the string
   representation for the period included by that date
 * PeriodType.start_end(period) returns a tuple of start date and end date for
   the given period
 * PeriodType.range(start, end) yields the periods from start to (but not
   including) stop. For example, period_range("Y-2010", "Y-2013") will yield
   "Y-2010", "Y-2011", "Y-2012".
 * PeriodType.display(period) displays the given period in a human-readable
   format

PERIOD_TYPES in this module maps the labels used for Period Types into the
classes themselves.

There are helper functions which dispatch to the right PeriodType for a given
period and call a class method on them:

 * period_start_end(period)
 * period_range(start, stop)
 * period_display(period)

There is also a helper function period_for_date which takes a period type name
like "weekly" and returns the period of the given date (or today if no date
given).
"""


class PeriodType(object):  # abstract base class

    validation_regex = r".*"
    minimum = None
    maximum = None

    @classmethod
    def validate(cls, period):
        regex = "^{}-".format(cls.prefix) + cls.validation_regex
        match = re.match(regex, period)
        if not match:
            raise ValidationError(
                "Incorrect value: {0}".format(period)
            )
        if match.groups():
            part = int(match.groups()[0])
            if cls.minimum and part < cls.minimum:
                raise ValidationError(
                    "Incorrect value: {0}".format(period)
                )
            if cls.maximum and part > cls.maximum:
                raise ValidationError(
                    "Incorrect value: {0}".format(period)
                )


class WeeklyPeriodType(PeriodType):

    prefix = "W"
    validation_regex = r"\d{4}-(\d{2})$"
    minimum = 1
    maximum = 53

    @classmethod
    def for_date(cls, date):
        year = date.isocalendar()[0]
        week = date.isocalendar()[1]
        return "{}-{:d}-{:02d}".format(cls.prefix, year, week)

    @classmethod
    def start_end(cls, period):
        year = int(period[2:6])
        week = int(period[7:])
        start = iso_week_to_gregorian(year, week)
        end = start + datetime.timedelta(days=6)
        return start, end

    @classmethod
    def range(cls, start, stop):
        cls.validate(start)
        cls.validate(stop)
        year_start = int(start[2:6])
        week_start = int(start[7:])
        year_stop = int(stop[2:6])
        week_stop = int(stop[7:])
        year = year_start
        week = week_start
        while (year, week) < (year_stop, week_stop):
            yield "{}-{:d}-{:02d}".format(cls.prefix, year, week)
            week += 1
            if datetime.date(year, 12, 31).isocalendar()[1] == 53:
                weeks_in_year = 53
            else:
                weeks_in_year = 52
            if week == weeks_in_year + 1:
                week = 1
                year += 1
        raise StopIteration()

    @classmethod
    def display(cls, period):
        year = int(period[2:6])
        week = int(period[7:])
        return iso_week_to_gregorian(year, week).strftime("Week of %b %d, %Y")


class QuarterlyPeriodType(PeriodType):

    prefix = "Q"
    validation_regex = r"\d{4}-(\d{1})$"
    minimum = 1
    maximum = 4

    @classmethod
    def for_date(cls, date):
        quarter = 1 + (date.month - 1) // 3
        return "{}-{:d}-{:d}".format(cls.prefix, date.year, quarter)

    @classmethod
    def start_end(cls, period):
        year = int(period[2:6])
        quarter = int(period[7])
        month = [None, 1, 4, 7, 10][quarter]
        end_month = calendar.monthrange(year, month + 2)[1]
        start = datetime.date(year, month, 1)
        end = datetime.date(year, month + 2, end_month)
        return start, end

    @classmethod
    def range(cls, start, stop):
        cls.validate(start)
        cls.validate(stop)
        year_start = int(start[2:6])
        quarter_start = int(start[7])
        year_stop = int(stop[2:6])
        quarter_stop = int(stop[7])
        year = year_start
        quarter = quarter_start
        while (year, quarter) < (year_stop, quarter_stop):
            yield "{}-{:d}-{:d}".format(cls.prefix, year, quarter)
            quarter += 1
            if quarter == 5:
                quarter = 1
                year += 1
        raise StopIteration()

    @classmethod
    def display(cls, period):
        year = int(period[2:6])
        quarter = int(period[7])
        return "{}Q{}".format(year, quarter)


class MonthlyPeriodType(PeriodType):

    prefix = "M"
    validation_regex = r"\d{4}-(\d{2})$"
    minimum = 1
    maximum = 12

    @classmethod
    def for_date(cls, date):
        return "{}-{:d}-{:02d}".format(cls.prefix, date.year, date.month)

    @classmethod
    def start_end(cls, period):
        year = int(period[2:6])
        month = int(period[7:])
        end_month = calendar.monthrange(year, month)[1]
        start = datetime.date(year, month, 1)
        end = datetime.date(year, month, end_month)
        return start, end

    @classmethod
    def range(cls, start, stop):
        cls.validate(start)
        cls.validate(stop)
        year_start = int(start[2:6])
        month_start = int(start[7:])
        year_stop = int(stop[2:6])
        month_stop = int(stop[7:])
        year = year_start
        month = month_start
        while (year, month) < (year_stop, month_stop):
            yield "{}-{:d}-{:02d}".format(cls.prefix, year, month)
            month += 1
            if month == 13:
                month = 1
                year += 1
        raise StopIteration()

    @classmethod
    def display(cls, period):
        year = int(period[2:6])
        month = int(period[7:])
        return "{} {}".format(month, year)  # @@@ month name


class YearlyPeriodType(PeriodType):

    prefix = "Y"
    validation_regex = r"\d{4}$"

    @classmethod
    def for_date(cls, date):
        return "{}-{:d}".format(cls.prefix, date.year)

    @classmethod
    def start_end(cls, period):
        year = int(period[2:])
        start = datetime.date(year, 1, 1)
        end = datetime.date(year, 12, 31)
        return start, end

    @classmethod
    def range(cls, start, stop):
        cls.validate(start)
        cls.validate(stop)
        year_start = int(start[2:])
        year_stop = int(stop[2:])
        year = year_start
        while year < year_stop:
            yield "{}-{:d}".format(cls.prefix, year)
            year += 1
        raise StopIteration()

    @classmethod
    def display(cls, period):
        year = int(period[2:])
        return "{}".format(year)


PERIOD_TYPES = {
    "weekly": WeeklyPeriodType,
    "quarterly": QuarterlyPeriodType,
    "monthly": MonthlyPeriodType,
    "yearly": YearlyPeriodType
}


PERIOD_PREFIXES = {
    period_type_class.prefix: period_type_class
    for period_type_class in PERIOD_TYPES.values()
}


def period_for_date(period_type, date=None):
    """
    for the given period_type, returns the period of the given date (or today
    if no second arg)
    """
    if date is None:
        date = timezone.now().date()
    return PERIOD_TYPES[period_type].for_date(date)


def period_start_end(period):
    """
    for the given period, return a tuple of the start and end dates
    """
    return PERIOD_PREFIXES[period[0]].start_end(period)


def period_range(start, stop):
    """
    yields the periods from start to (but not including) stop.

    For example, period_range("Y-2010", "Y-2013") will yield "Y-2010",
    "Y-2011", "Y-2012".
    """
    if start[0] != stop[0]:
        raise ValidationError("start and stop must be of same period type")
    return PERIOD_PREFIXES[start[0]].range(start, stop)


def period_display(period):
    """
    display the given period in a human-readable form
    """
    return PERIOD_PREFIXES[period[0]].display(period)


def iso_week_to_gregorian(iso_year, iso_week):
    fourth_jan = datetime.date(iso_year, 1, 4)
    year_start = fourth_jan - datetime.timedelta(fourth_jan.isoweekday() - 1)
    return year_start + datetime.timedelta(weeks=iso_week - 1)
