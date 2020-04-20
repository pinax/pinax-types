![](http://pinaxproject.com/pinax-design/patches/pinax-types.svg)

# Pinax Types

[![](https://img.shields.io/pypi/v/pinax-types.svg)](https://pypi.python.org/pypi/pinax-types/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-types.svg)](https://circleci.com/gh/pinax/pinax-types)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-types.svg)](https://codecov.io/gh/pinax/pinax-types)
[![](https://img.shields.io/github/contributors/pinax/pinax-types.svg)](https://github.com/pinax/pinax-types/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-types.svg)](https://github.com/pinax/pinax-types/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-types.svg)](https://github.com/pinax/pinax-types/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


## Table of Contents

* [About Pinax](#about-pinax)
* [Important Links](#important-links)
* [Overview](#overview)
  * [Supported Django and Python Versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Usage](#usage)
* [Change Log](#change-log)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.


## Important Links

Where you can find what you need:
* Releases: published to [PyPI](https://pypi.org/search/?q=pinax) or tagged in app repos in the [Pinax GitHub organization](https://github.com/pinax/)
* Global documentation: [Pinax documentation website](https://pinaxproject.com/pinax/)
* App specific documentation: app repos in the [Pinax GitHub organization](https://github.com/pinax/)
* Support information: [SUPPORT.md](https://github.com/pinax/.github/blob/master/SUPPORT.md) file in the [Pinax default community health file repo](https://github.com/pinax/.github/)
* Contributing information: [CONTRIBUTING.md](https://github.com/pinax/.github/blob/master/CONTRIBUTING.md) file in the [Pinax default community health file repo](https://github.com/pinax/.github/)
* Current and historical release docs: [Pinax Wiki](https://github.com/pinax/pinax/wiki/)


## pinax-types

### Overview

#### Supported Django and Python Versions

Django / Python | 3.6 | 3.7 | 3.8
--------------- | --- | --- | ---
2.2  |  *  |  *  |  *
3.0  |  *  |  *  |  *


## Documentation

### Installation

To install pinax-types:

```shell
    $ pip install python-dateutil pinax-types
```

Add `pinax.types` to your `INSTALLED_APPS` setting:

```python
    INSTALLED_APPS = [
        # other apps
        "pinax.types",
    ]
```

### Usage

#### Value Types

Value Types define the type a metric or indicator's values can take.

While all measurement and calculated values are stored in the database as
Decimals, the interpretation, validation and display of those values is
determined by class methods on the Value Type classes here.

 * `ValueType.validate(value)` validates whether value is valid for this type
 * `ValueType.template_name()` returns the template name to use for indicators
   of this type
 * `ValueType.display()` formats the value as a string appropriately

`VALUE_TYPES` in this module maps the labels used for Value Types into the
classes themselves.

#### Period Types

Period Types define different periods over which metrics can apply, e.g. weeks,
months or quarters.

 * `PeriodType.validate(period)` validates whether a string representation is
   valid for this period type
 * `PeriodType.for_date(date)` converts a `datetime.date` to the string
   representation for the period included by that date
 * `PeriodType.start_end(period)` returns a tuple of start date and end date for
   the given period
 * `PeriodType.range(start, end)` yields the periods from start to (but not
   including) stop. For example, `period_range("Y-2010", "Y-2013")` will yield
   `"Y-2010", "Y-2011", "Y-2012"`.
 * `PeriodType.display(period)` displays the given period in a human-readable
   format

`PERIOD_TYPES` in this module maps the labels used for Period Types into the
classes themselves.

There are helper functions which dispatch to the right `PeriodType` for a given
period and call a class method on them:

 * `period_start_end(period)`
 * `period_range(start, stop)`
 * `period_display(period)`

There is also a helper function `period_for_date` which takes a period type name
like "weekly" and returns the period of the given date (or today if no date
given).


## Change Log

### 2.0.0

* Drop Django 1.11, 2.0, and 2.1, and Python 2,7, 3.4, and 3.5 support
* Add Django 2.2 and 3.0, and Python 3.6, 3.7, and 3.8 support
* Update packaging configs
* Direct users to community resources

### 1.0.0

* Add Django 2.0 compatibility testing
* Drop Django 1.8, 1.9, 1.10, and Python 3.3 support
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description
* Move documentation to README.md


## Contribute

[Contributing](https://github.com/pinax/.github/blob/master/CONTRIBUTING.md) information can be found in the [Pinax community health file repo](https://github.com/pinax/.github).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a [Code of Conduct](https://github.com/pinax/.github/blob/master/CODE_OF_CONDUCT.md). We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject) and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-present James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).
