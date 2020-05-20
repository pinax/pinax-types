from setuptools import find_packages, setup

VERSION = "2.0.0"
LONG_DESCRIPTION = """
.. image:: http://pinaxproject.com/pinax-design/patches/pinax-types.svg
    :target: https://pypi.python.org/pypi/pinax-types/

===========
Pinax Types
===========

.. image:: https://img.shields.io/pypi/v/pinax-types.svg
    :target: https://pypi.python.org/pypi/pinax-types/

\

.. image:: https://img.shields.io/circleci/project/github/pinax/pinax-types.svg
    :target: https://circleci.com/gh/pinax/pinax-types
.. image:: https://img.shields.io/codecov/c/github/pinax/pinax-types.svg
    :target: https://codecov.io/gh/pinax/pinax-types
.. image:: https://img.shields.io/github/contributors/pinax/pinax-types.svg
    :target: https://github.com/pinax/pinax-types/graphs/contributors
.. image:: https://img.shields.io/github/issues-pr/pinax/pinax-types.svg
    :target: https://github.com/pinax/pinax-types/pulls
.. image:: https://img.shields.io/github/issues-pr-closed/pinax/pinax-types.svg
    :target: https://github.com/pinax/pinax-types/pulls?q=is%3Apr+is%3Aclosed

\

.. image:: http://slack.pinaxproject.com/badge.svg
    :target: http://slack.pinaxproject.com/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT/

\

Supported Django and Python Versions
------------------------------------

+-----------------+-----+-----+-----+
| Django / Python | 3.6 | 3.7 | 3.8 |
+=================+=====+=====+=====+
|  2.2            |  *  |  *  |  *  |
+-----------------+-----+-----+-----+
|  3.0            |  *  |  *  |  *  |
+-----------------+-----+-----+-----+
"""

setup(
    author="Pinax Team",
    author_email="team@pinaxproject.com",
    description="<project description> for the Django web framework",
    name="pinax-types",
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    url="http://github.com/pinax/pinax-types/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "pinax.types": []
    },
    test_suite="runtests.runtests",
    tests_require=[
        "python-dateutil>=2.8.1"
    ],
    install_requires=[
        "django>=2.2",
        "python-dateutil>=2.8.1"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
