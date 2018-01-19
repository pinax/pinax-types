from setuptools import find_packages, setup

LONG_DESCRIPTION = """
.. image:: http://pinaxproject.com/pinax-design/patches/pinax-types.svg
    :target: https://pypi.python.org/pypi/pinax-types/
    
===================
Pinax Notifications
===================

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

+-----------------+-----+-----+-----+-----+
| Django \ Python | 2.7 | 3.4 | 3.5 | 3.6 |
+=================+=====+=====+=====+=====+
| 1.11            |  *  |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
| 2.0             |     |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
"""

setup(
    author="Pinax Team",
    author_email="team@pinaxprojects.com",
    description="<project description> for the Django web framework",
    name="pinax-types",
    long_description=LONG_DESCRIPTION,
    version="1.0.0",
    url="http://github.com/pinax/pinax-types/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "pinax.types": []
    },
    test_suite="runtests.runtests",
    tests_require=[
        "python-dateutil>=2.4.0"
    ],
    install_required=[
        "python-dateutil>=2.4.0"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
