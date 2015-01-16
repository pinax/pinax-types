import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.test import TestCase

from pinax.types.values import VALUE_TYPES
from pinax.types.periods import PERIOD_TYPES, validate, parse, get_period, period_for_date, period_range, period_display, period_start_end


class ValueTypesTests(TestCase):

    def test_integer_value_type_raises_error(self):
        with self.assertRaises(ValidationError):
            VALUE_TYPES["integer"].validate("foo")

    def test_integer_value_type_validates(self):
        self.assertIsNone(VALUE_TYPES["integer"].validate("566"))

    def test_boolean_value_type_raises_error_on_not_true_or_false(self):
        with self.assertRaises(ValidationError):
            VALUE_TYPES["boolean"].validate("foo")

    def test_boolean_value_type_validates_true(self):
        self.assertIsNone(VALUE_TYPES["boolean"].validate("true"))

    def test_boolean_value_type_validates_false(self):
        self.assertIsNone(VALUE_TYPES["boolean"].validate("false"))

    def test_decimal_value_type_raises_error(self):
        with self.assertRaises(ValidationError):
            VALUE_TYPES["decimal"].validate("foo")

    def test_decimal_value_type_validates(self):
        self.assertIsNone(VALUE_TYPES["decimal"].validate("5.66"))

    def test_monetary_value_type_raises_error(self):
        with self.assertRaises(ValidationError):
            VALUE_TYPES["monetary"].validate("foo")

    def test_monetary_value_type_validates(self):
        self.assertIsNone(VALUE_TYPES["monetary"].validate("56.60"))

    def test_hour_value_type_raises_error(self):
        with self.assertRaises(ValidationError):
            VALUE_TYPES["hours"].validate("foo")

    def test_hour_value_type_validates(self):
        self.assertIsNone(VALUE_TYPES["hours"].validate("56"))

    def test_traffic_light_value_type_raises_error_on_big_int(self):
        with self.assertRaises(ValidationError):
            VALUE_TYPES["traffic-light"].validate("1000")

    def test_traffic_light_value_type_raises_error_on_non_int(self):
        with self.assertRaises(ValidationError):
            VALUE_TYPES["traffic-light"].validate("foo")

    def test_traffic_light_value_type_validates(self):
        self.assertIsNone(VALUE_TYPES["traffic-light"].validate("2"))

    def test_monetary_value_display(self):
        self.assertEquals(VALUE_TYPES["monetary"].display(1000), "$1,000")

    def test_percentage_value_display(self):
        self.assertEquals(VALUE_TYPES["percentage"].display(0.37), "37.0%")

    def test_hours_value_display(self):
        self.assertEquals(VALUE_TYPES["hours"].display(1000), "1000h")

    def test_traffic_light_value_display(self):
        self.assertEquals(VALUE_TYPES["traffic-light"].display(1), "red")


class PeriodTests(TestCase):

    def setUp(self):
        self.quarter_1 = get_period("Q-2015-1")
        self.quarter_2 = get_period("Q-2015-2")
        self.year = get_period("Y-2015")

    def test_quarterly_sub_periods_monthly_all(self):
        periods = self.quarter_1.sub_periods("monthly")
        self.assertEquals(len(periods), 3)
        self.assertEquals(periods[0].get_display(), "January 2015")
        self.assertEquals(periods[1].get_display(), "February 2015")
        self.assertEquals(periods[2].get_display(), "March 2015")

    def test_quarterly_sub_periods_weekly_all(self):
        periods = self.quarter_1.sub_periods("weekly")
        self.assertEquals(len(periods), 14)
        self.assertEquals(periods[0].raw_value, "W-2015-01")
        self.assertEquals(periods[1].raw_value, "W-2015-02")
        self.assertEquals(periods[2].raw_value, "W-2015-03")
        self.assertEquals(periods[3].raw_value, "W-2015-04")
        self.assertEquals(periods[4].raw_value, "W-2015-05")
        self.assertEquals(periods[5].raw_value, "W-2015-06")
        self.assertEquals(periods[6].raw_value, "W-2015-07")
        self.assertEquals(periods[7].raw_value, "W-2015-08")
        self.assertEquals(periods[8].raw_value, "W-2015-09")
        self.assertEquals(periods[9].raw_value, "W-2015-10")
        self.assertEquals(periods[10].raw_value, "W-2015-11")
        self.assertEquals(periods[11].raw_value, "W-2015-12")
        self.assertEquals(periods[12].raw_value, "W-2015-13")
        self.assertEquals(periods[13].raw_value, "W-2015-14")

    def test_yearly_sub_periods_quarterly_all(self):
        periods = get_period("Y-2015").sub_periods("quarterly")
        self.assertEquals(len(periods), 4)
        self.assertEquals(periods[0].raw_value, "Q-2015-1")
        self.assertEquals(periods[1].raw_value, "Q-2015-2")
        self.assertEquals(periods[2].raw_value, "Q-2015-3")
        self.assertEquals(periods[3].raw_value, "Q-2015-4")

    def test_yearly_sub_periods_monthly_all(self):
        periods = get_period("Y-2015").sub_periods("monthly")
        self.assertEquals(len(periods), 12)
        self.assertEquals(periods[0].get_display(), "January 2015")
        self.assertEquals(periods[1].get_display(), "February 2015")
        self.assertEquals(periods[2].get_display(), "March 2015")
        self.assertEquals(periods[3].get_display(), "April 2015")
        self.assertEquals(periods[4].get_display(), "May 2015")
        self.assertEquals(periods[5].get_display(), "June 2015")
        self.assertEquals(periods[6].get_display(), "July 2015")
        self.assertEquals(periods[7].get_display(), "August 2015")
        self.assertEquals(periods[8].get_display(), "September 2015")
        self.assertEquals(periods[9].get_display(), "October 2015")
        self.assertEquals(periods[10].get_display(), "November 2015")
        self.assertEquals(periods[11].get_display(), "December 2015")

    def test_yearly_sub_periods_weekly_all(self):
        periods = get_period("Y-2015").sub_periods("weekly")
        self.assertEquals(len(periods), 53)
        for i in range(53):
            self.assertEquals(periods[i].raw_value, "W-2015-{:02d}".format(i + 1))

    def test_monthly_sub_periods_weekly_all(self):
        periods = get_period("M-2015-01").sub_periods("weekly")
        self.assertEquals(len(periods), 5)
        for i in range(5):
            self.assertEquals(periods[i].raw_value, "W-2015-{:02d}".format(i + 1))

    def test_validate_for_pass(self):
        try:
            self.quarter_1.validate_for("quarterly")
        except ValidationError:
            self.fail()

    def test_validate_for_fail(self):
        with self.assertRaises(ValidationError):
            self.quarter_1.validate_for("weekly")

    def test_validate_can_contain_type_pass_1(self):
        try:
            self.quarter_1.validate_can_contain_type("quarterly")
        except ValidationError:
            self.fail()

    def test_validate_can_contain_type_pass_2(self):
        try:
            self.quarter_1.validate_can_contain_type("weekly")
        except ValidationError:
            self.fail()

    def test_validate_can_contain_type_faik(self):
        with self.assertRaises(ValidationError):
            self.quarter_1.validate_can_contain_type("yearly")

    def test_get_display(self):
        self.assertEquals(get_period("M-2015-04").get_display(), "April 2015")

    def test_current(self):
        period = get_period(PERIOD_TYPES["quarterly"].for_date(timezone.now()))
        self.assertTrue(period.is_current())

    def test_past(self):
        period = get_period("M-2013-11")
        self.assertTrue(period.is_past())

    def test_includes_1(self):
        self.assertTrue(self.year.includes(self.quarter_1))
        self.assertTrue(self.year.includes(self.quarter_2))

    def test_includes_2(self):
        self.assertFalse(self.quarter_1.includes(self.year))

    def test_includes_3(self):
        self.assertFalse(self.quarter_1.includes(self.quarter_2))

    def test_includes_4(self):
        self.assertTrue(self.quarter_1.includes(get_period("Q-2015-1")))

    def test_validate_random_string(self):
        with self.assertRaises(ValidationError):
            validate("Patrick")

    def test_equality_true(self):
        self.assertTrue(self.quarter_1 == get_period("Q-2015-1"))

    def test_equality_false_1(self):
        self.assertFalse(self.quarter_1 == self.quarter_2)

    def test_equality_false_2(self):
        self.assertFalse(self.quarter_1 == self.year)

    def test_non_equality_false(self):
        self.assertFalse(self.quarter_1 != get_period("Q-2015-1"))

    def test_non_equality_true_1(self):
        self.assertTrue(self.quarter_1 != self.quarter_2)

    def test_non_equality_true_2(self):
        self.assertTrue(self.quarter_1 != self.year)

    def test_less_than_true(self):
        self.assertTrue(self.quarter_1 < self.quarter_2)

    def test_less_than_false_1(self):
        self.assertFalse(self.quarter_2 < self.quarter_1)

    def test_less_than_false_2(self):
        self.assertFalse(self.quarter_1 < self.year)

    def test_greater_than_true(self):
        self.assertTrue(self.quarter_2 > self.quarter_1)

    def test_greater_than_false_1(self):
        self.assertFalse(self.quarter_1 > self.quarter_2)

    def test_greater_than_false_2(self):
        self.assertFalse(self.quarter_1 > self.year)

    def test_less_than_or_equal_true(self):
        self.assertTrue(self.quarter_1 <= self.quarter_2)

    def test_less_than_or_equal_false_1(self):
        self.assertFalse(self.quarter_2 <= self.quarter_1)

    def test_less_than_or_equal_false_2(self):
        self.assertFalse(self.quarter_1 <= self.year)

    def test_greater_than_or_equal_true(self):
        self.assertTrue(self.quarter_2 >= self.quarter_1)

    def test_greater_than_or_equal_false_1(self):
        self.assertFalse(self.quarter_1 >= self.quarter_2)

    def test_greater_than_or_equal_false_2(self):
        self.assertFalse(self.quarter_1 >= self.year)

    def test_parse_week_1(self):
        self.assertEquals(parse("2015-W03"), "W-2015-03")

    def test_parse_week_2(self):
        self.assertEquals(parse("2015-W3"), "W-2015-03")

    def test_parse_week_3(self):
        self.assertEquals(parse("2015W03"), "W-2015-03")

    def test_parse_week_4(self):
        self.assertEquals(parse("2015W3"), "W-2015-03")

    def test_parse_month_1(self):
        self.assertEquals(parse("jan 2015"), "M-2015-01")

    def test_parse_month_2(self):
        self.assertEquals(parse("Jan 2015"), "M-2015-01")

    def test_parse_month_3(self):
        self.assertEquals(parse("January 2015"), "M-2015-01")

    def test_parse_month_4(self):
        self.assertEquals(parse("1/2015"), "M-2015-01")

    def test_parse_month_5(self):
        self.assertEquals(parse("01/2015"), "M-2015-01")

    def test_parse_month_6(self):
        self.assertEquals(parse("2015 January"), "M-2015-01")

    def test_parse_quarter_1(self):
        self.assertEquals(parse("2015Q1"), "Q-2015-1")

    def test_parse_quarter_2(self):
        self.assertEquals(parse("2015Q1"), "Q-2015-1")

    def test_parse_quarter_3(self):
        with self.assertRaises(ValidationError):
            self.assertEquals(parse("2015Q5"), "Q-2015-5")

    def test_parse_year_1(self):
        self.assertEquals(parse("2015"), "Y-2015")

    def test_parse_invalid(self):
        self.assertIsNone(parse("Patrick"))

    def test_get_period_str(self):
        period = get_period("M-2015-01")
        self.assertEquals(str(period), "M-2015-01")

    def test_get_period_validation(self):
        with self.assertRaises(ValidationError):
            get_period("2013W22")

    def test_weekly_period_type_raises_error_wrong_format(self):
        with self.assertRaises(ValidationError):
            PERIOD_TYPES["weekly"].validate("2013W22")

    def test_weekly_period_type_raises_error_week_number_too_low(self):
        with self.assertRaises(ValidationError):
            PERIOD_TYPES["weekly"].validate("W-2013-00")

    def test_weekly_period_type_raises_error_week_number_too_high(self):
        with self.assertRaises(ValidationError):
            PERIOD_TYPES["weekly"].validate("W-2013-75")

    def test_weekly_period_type_validates_week(self):
        self.assertIsNone(PERIOD_TYPES["weekly"].validate("W-2013-22"))

    def test_monthly_period_type_raises_error_wrong_format(self):
        with self.assertRaises(ValidationError):
            PERIOD_TYPES["monthly"].validate("201312")

    def test_monthly_period_type_raises_error_wrong_week_number(self):
        with self.assertRaises(ValidationError):
            PERIOD_TYPES["monthly"].validate("M-2013-15")

    def test_monthly_period_type_validates_week(self):
        self.assertIsNone(PERIOD_TYPES["monthly"].validate("M-2013-12"))

    def test_quarterly_period_type_raises_error_wrong_format(self):
        with self.assertRaises(ValidationError):
            PERIOD_TYPES["quarterly"].validate("2013Q4")

    def test_quarterly_period_type_raises_error_wrong_week_number(self):
        with self.assertRaises(ValidationError):
            PERIOD_TYPES["quarterly"].validate("Q-20139")

    def test_quarterly_period_type_validates_week(self):
        self.assertIsNone(PERIOD_TYPES["quarterly"].validate("Q-2013-3"))

    def test_yearly_period_type_raises_error_wrong_format(self):
        with self.assertRaises(ValidationError):
            PERIOD_TYPES["yearly"].validate("2013")

    def test_yearly_period_type_raises_error_wrong_week_number(self):
        with self.assertRaises(ValidationError):
            PERIOD_TYPES["yearly"].validate("Y-20139")

    def test_yearly_period_type_validates_week(self):
        self.assertIsNone(PERIOD_TYPES["yearly"].validate("Y-2013"))

    def test_weekly_period_for_date_end_of_year(self):
        self.assertEquals(period_for_date("weekly", datetime.date(2014, 12, 27)), "W-2014-52")

    def test_weekly_period_for_date_start_of_year(self):
        self.assertEquals(period_for_date("weekly", datetime.date(2014, 12, 30)), "W-2015-01")

    def test_weekly_period_for_date(self):
        self.assertEquals(period_for_date("weekly", datetime.date(2013, 8, 7)), "W-2013-32")

    def test_quarterly_period_for_date(self):
        self.assertEquals(period_for_date("quarterly", datetime.date(2013, 8, 7)), "Q-2013-3")

    def test_monthly_period_for_date(self):
        self.assertEquals(period_for_date("monthly", datetime.date(2013, 8, 7)), "M-2013-08")

    def test_yearly_period_for_date(self):
        self.assertEquals(period_for_date("yearly", datetime.date(2013, 8, 7)), "Y-2013")

    def test_period_for_date_today(self):
        self.assertEquals(period_for_date("yearly"), "Y-{}".format(datetime.date.today().year))

    def test_weekly_period_range(self):
        self.assertEquals(list(period_range("W-2012-50", "W-2013-03")), ["W-2012-50", "W-2012-51", "W-2012-52", "W-2013-01", "W-2013-02"])
        self.assertEquals(list(period_range("W-2014-50", "W-2015-03")), ["W-2014-50", "W-2014-51", "W-2014-52", "W-2015-01", "W-2015-02"])
        self.assertEquals(list(period_range("W-2015-50", "W-2016-03")), ["W-2015-50", "W-2015-51", "W-2015-52", "W-2015-53", "W-2016-01", "W-2016-02"])
        self.assertEquals(list(period_range("W-2016-50", "W-2017-03")), ["W-2016-50", "W-2016-51", "W-2016-52", "W-2017-01", "W-2017-02"])

    def test_weekly_period_inclusive_range(self):
        self.assertEquals(list(period_range("W-2012-50", "W-2013-03", inclusive=True)), ["W-2012-50", "W-2012-51", "W-2012-52", "W-2013-01", "W-2013-02", "W-2013-03"])
        self.assertEquals(list(period_range("W-2014-50", "W-2015-03", inclusive=True)), ["W-2014-50", "W-2014-51", "W-2014-52", "W-2015-01", "W-2015-02", "W-2015-03"])
        self.assertEquals(list(period_range("W-2015-50", "W-2016-03", inclusive=True)), ["W-2015-50", "W-2015-51", "W-2015-52", "W-2015-53", "W-2016-01", "W-2016-02", "W-2016-03"])
        self.assertEquals(list(period_range("W-2016-50", "W-2017-03", inclusive=True)), ["W-2016-50", "W-2016-51", "W-2016-52", "W-2017-01", "W-2017-02", "W-2017-03"])

    def test_monthly_period_range(self):
        self.assertEquals(list(period_range("M-2012-11", "M-2013-03")), ["M-2012-11", "M-2012-12", "M-2013-01", "M-2013-02"])

    def test_monthly_period_inclusive_range(self):
        self.assertEquals(list(period_range("M-2012-11", "M-2013-03", inclusive=True)), ["M-2012-11", "M-2012-12", "M-2013-01", "M-2013-02", "M-2013-03"])

    def test_quarterly_period_range(self):
        self.assertEquals(list(period_range("Q-2012-3", "Q-2013-2")), ["Q-2012-3", "Q-2012-4", "Q-2013-1"])

    def test_quarterly_period_inclusive_range(self):
        self.assertEquals(list(period_range("Q-2012-3", "Q-2013-2", inclusive=True)), ["Q-2012-3", "Q-2012-4", "Q-2013-1", "Q-2013-2"])

    def test_yearly_period_range(self):
        self.assertEquals(list(period_range("Y-2010", "Y-2013")), ["Y-2010", "Y-2011", "Y-2012"])

    def test_yearly_period_range_inclusive(self):
        self.assertEquals(list(period_range("Y-2010", "Y-2013", inclusive=True)), ["Y-2010", "Y-2011", "Y-2012", "Y-2013"])

    def test_period_range_mismatched_types(self):
        with self.assertRaises(ValidationError):
            period_range("W-2012-50", "Y-2013")

    def test_yearly_period_type_display(self):
        self.assertEquals(period_display("Y-2013"), "2013")

    def test_monthly_period_type_display(self):
        self.assertEquals(period_display("M-2013-08"), "August 2013")

    def test_quarterly_period_type_display(self):
        self.assertEquals(period_display("Q-2013-3"), "2013Q3")

    def test_weekly_period_type_display(self):
        self.assertEquals(period_display("W-2013-32"), "Week of Aug 05, 2013")

    def test_yearly_period_type_start_end(self):
        self.assertEquals(period_start_end("Y-2013"), (datetime.date(2013, 1, 1), datetime.date(2013, 12, 31)))

    def test_monthly_period_type_start_end(self):
        self.assertEquals(period_start_end("M-2013-08"), (datetime.date(2013, 8, 1), datetime.date(2013, 8, 31)))

    def test_quarterly_period_type_start_end(self):
        self.assertEquals(period_start_end("Q-2013-3"), (datetime.date(2013, 7, 1), datetime.date(2013, 9, 30)))

    def test_weekly_period_type_start_end(self):
        self.assertEquals(period_start_end("W-2013-32"), (datetime.date(2013, 8, 5), datetime.date(2013, 8, 11)))
