import calendar
import datetime
import operator
import re

from django.core.exceptions import ValidationError

from dateutil.parser import parse as dateutil_parse


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


class Period(object):  # abstract base class

    prefix = None
    validation_regex = r".*"
    minimum = None
    maximum = None
    contains = []

    def __init__(self, raw_value):
        self.validate(raw_value)
        self.raw_value = raw_value

    def __str__(self):
        return self.raw_value

    def includes(self, period):
        """
        quarter.includes(month) : True|False
        """
        if self == period:
            return True
        if period.prefix in self.contains:
            start, end = self.start_end(self.raw_value)
            start2, end2 = period.start_end(period.raw_value)
            return start <= start2 and end >= end2
        return False

    def sub_periods(self, period_type):
        self.validate_can_contain_type(period_type)
        periods = []
        if self.is_period_type(period_type):
            periods.append(get_period(self.raw_value))
        klass = PERIOD_TYPES[period_type]
        start, end = self.get_start_end()
        start, end = klass.for_date(start), klass.for_date(end)
        for period_raw in klass.range(start, end, inclusive=True):
            periods.append(get_period(period_raw))
        return periods

    def validate_can_contain_type(self, period_type):
        valids = [x.upper() for x in (self.contains + [self.prefix])]
        if period_type[0].upper() not in valids:
            raise ValidationError(
                "Periods of the type {} cannot exist within {}".format(
                    period_type,
                    ", ".join(valids)
                )
            )

    def is_period_type(self, period_type):
        return period_type[0].upper() == self.prefix.upper()

    def validate_for(self, period_type):
        if not self.is_period_type(period_type):
            raise ValidationError(
                "{} must match this period's ({}) type".format(
                    period_type.title(),
                    self.get_display()
                )
            )

    def get_start_end(self):
        return self.start_end(self.raw_value)

    def get_display(self):
        return self.display(self.raw_value)

    @classmethod
    def current_period(cls):
        current = cls.for_date(datetime.datetime.now())
        return get_period(current)

    def is_past(self):
        return self.current_period() > self

    def is_current(self):
        return self.current_period() == self

    def is_future(self):
        return self.current_period() < self

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

    def __eq__(self, other):
        return type(self) == type(other) and self.raw_value == other.raw_value

    def __ne__(self, other):
        return type(self) != type(other) or self.raw_value != other.raw_value

    def __lt__(self, other):
        # @@@ we might want to be smart and be able to do things like "Q-2014-Q4" < "Y-2015"
        return type(self) == type(other) and self.raw_value < other.raw_value

    def __gt__(self, other):
        return type(self) == type(other) and self.raw_value > other.raw_value

    def __le__(self, other):
        return type(self) == type(other) and self.raw_value <= other.raw_value

    def __ge__(self, other):
        return type(self) == type(other) and self.raw_value >= other.raw_value


class WeeklyPeriod(Period):

    prefix = "W"
    validation_regex = r"\d{4}-(\d{2})$"
    minimum = 1
    maximum = 53

    @classmethod
    def from_parts(cls, year, week):
        return "{}-{:d}-{:02d}".format(cls.prefix, int(year), int(week))

    @classmethod
    def for_date(cls, date):
        year = date.isocalendar()[0]
        week = date.isocalendar()[1]
        return cls.from_parts(year, week)

    @classmethod
    def start_end(cls, period):
        year = int(period[2:6])
        week = int(period[7:])
        start = iso_week_to_gregorian(year, week)
        end = start + datetime.timedelta(days=6)
        return start, end

    @classmethod
    def range(cls, start, stop, inclusive=False):
        cls.validate(start)
        cls.validate(stop)
        year_start = int(start[2:6])
        week_start = int(start[7:])
        year_stop = int(stop[2:6])
        week_stop = int(stop[7:])
        year = year_start
        week = week_start
        op = operator.le if inclusive else operator.lt
        while op((year, week), (year_stop, week_stop)):
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


class QuarterlyPeriod(Period):

    prefix = "Q"
    validation_regex = r"\d{4}-(\d{1})$"
    minimum = 1
    maximum = 4
    contains = ["M", "W"]

    @classmethod
    def from_parts(cls, year, quarter):
        return "{}-{:d}-{:d}".format(cls.prefix, int(year), int(quarter))

    @classmethod
    def for_date(cls, date):
        quarter = 1 + (date.month - 1) // 3
        return cls.from_parts(date.year, quarter)

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
    def range(cls, start, stop, inclusive=False):
        cls.validate(start)
        cls.validate(stop)
        year_start = int(start[2:6])
        quarter_start = int(start[7])
        year_stop = int(stop[2:6])
        quarter_stop = int(stop[7])
        year = year_start
        quarter = quarter_start
        op = operator.le if inclusive else operator.lt
        while op((year, quarter), (year_stop, quarter_stop)):
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


class MonthlyPeriod(Period):

    prefix = "M"
    validation_regex = r"\d{4}-(\d{2})$"
    minimum = 1
    maximum = 12
    contains = ["W"]

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
    def range(cls, start, stop, inclusive=False):
        cls.validate(start)
        cls.validate(stop)
        year_start = int(start[2:6])
        month_start = int(start[7:])
        year_stop = int(stop[2:6])
        month_stop = int(stop[7:])
        year = year_start
        month = month_start
        op = operator.le if inclusive else operator.lt
        while op((year, month), (year_stop, month_stop)):
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
        return datetime.date(year, month, 1).strftime("%B %Y")


class YearlyPeriod(Period):

    prefix = "Y"
    validation_regex = r"\d{4}$"
    contains = ["Q", "M", "W"]

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
    def range(cls, start, stop, inclusive=False):
        cls.validate(start)
        cls.validate(stop)
        year_start = int(start[2:])
        year_stop = int(stop[2:])
        year = year_start
        op = operator.le if inclusive else operator.lt
        while op(year, year_stop):
            yield "{}-{:d}".format(cls.prefix, year)
            year += 1
        raise StopIteration()

    @classmethod
    def display(cls, period):
        year = int(period[2:])
        return "{}".format(year)


PREFIXES = {
    "W": WeeklyPeriod,
    "M": MonthlyPeriod,
    "Q": QuarterlyPeriod,
    "Y": YearlyPeriod
}

PERIOD_TYPES = {
    "weekly": WeeklyPeriod,
    "quarterly": QuarterlyPeriod,
    "monthly": MonthlyPeriod,
    "yearly": YearlyPeriod
}

PERIOD_TYPE_CHOICES = [
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
    ("quarterly", "Quarterly"),
    ("yearly", "Yearly")
]

PERIOD_PREFIXES = {
    period_type_class.prefix: period_type_class
    for period_type_class in PERIOD_TYPES.values()
}


def parse(value):
    """
    Convert:

    * 2015-W3, 2015-W03, 2015W03, 2015W3 ==> W-2015-03
    * 1/2015, 01/2015, Jan 2015, January 2015 ==> M-2015-01
    * 2015Q1 ==> Q-2015-1
    * 2015 ==> Y-2015
    """
    result = None
    if len(value) in [6, 7, 8] and value[:4].isdigit() and "W" in value and value.index("W") in [4, 5] and value[value.index("W") + 1:].isdigit():
        year, week = value[:4], value[value.index("W") + 1:]
        result = WeeklyPeriod.from_parts(year, week)
    elif len(value) == 6 and value[:4].isdigit() and value[4].lower() == "q" and value[5].isdigit():
        year, quarter = value[:4], value[5]
        result = QuarterlyPeriod.from_parts(year, quarter)
    elif len(value) == 4 and value.isdigit():
        result = YearlyPeriod.for_date(dateutil_parse(value))
    else:
        try:
            result = MonthlyPeriod.for_date(dateutil_parse(value))
        except ValueError:
            pass
    if result:
        validate(result)
    return result


def validate(raw_value):
    if raw_value[0] not in PERIOD_PREFIXES:
        raise ValidationError("invalid prefix in {}".format(raw_value))
    return PERIOD_PREFIXES[raw_value[0]].validate(raw_value)


def get_period(raw_value):
    if raw_value[0] not in PERIOD_PREFIXES:
        raise ValidationError("invalid prefix in {}".format(raw_value))
    return PERIOD_PREFIXES[raw_value[0]](raw_value)


def period_for_date(period_type, date=None):
    """
    for the given period_type, returns the period of the given date (or today
    if no second arg)
    """
    if date is None:
        date = datetime.datetime.now().date()
    return PERIOD_TYPES[period_type].for_date(date)


def period_start_end(period):
    """
    for the given period, return a tuple of the start and end dates
    """
    return PERIOD_PREFIXES[period[0]].start_end(period)


def period_range(start, stop, inclusive=False):
    """
    yields the periods from start to (but not including) stop.

    For example, period_range("Y-2010", "Y-2013") will yield "Y-2010",
    "Y-2011", "Y-2012".
    """
    if start[0] != stop[0]:
        raise ValidationError("start and stop must be of same period type")
    return PERIOD_PREFIXES[start[0]].range(start, stop, inclusive)


def period_display(period):
    """
    display the given period in a human-readable form
    """
    return PERIOD_PREFIXES[period[0]].display(period)


def iso_week_to_gregorian(iso_year, iso_week):
    fourth_jan = datetime.date(iso_year, 1, 4)
    year_start = fourth_jan - datetime.timedelta(fourth_jan.isoweekday() - 1)
    return year_start + datetime.timedelta(weeks=iso_week - 1)
