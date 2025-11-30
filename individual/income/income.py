#!/usr/env/bin python3
#coding:utf-8

"""
Income

This package contains functions that compute taxable portions of various income
sources (such as Social Security) and other information needed to populate the
Income section of the 1040. The client program is responsible for figuring the
adjusted gross income and taxable income.
"""

def taxable_dep_care(benefits, expenses):
    """
    taxable_dep_care computes the amount of dependent care benefits that are
    subject to income tax. This information is reported on Part III of form 2441
    on line 26.

    The amount of dependent care benefits provided to the employee can be found
    on form W-2 box 10.
    """
    return 0

def taxable_adoption_benefits():
    return 0

def taxable_ss(income, filingStatus):
    """
    taxable_ss computes the taxable portion of social security benefits using
    income information from the 1040 and Schedule 1. This information is given
    as a dictionary of the following form:

    {
        <form>: {
            <line>: <value>
        }
    }

    for example:

    {
        'SSA-1099': {
            'Box5': 42000
        },
        '1040': {
            '1z': 20000
        }
    }

    This is more structure than strictly necessary, but makes the relationship
    to the Social Security Benefits Worksheet found in the 1040 instructions a
    bit clearer.

    Input
        income dict(string) float: A dictionary containing the relevant income
        information needed to compute the taxable portion of SS benefits.

    Output
        The taxable portion of Social Security benefits


    Examples

    >>> taxable_ss({ 'SSA-1099': 65000 }, 'S')
    0
    """
    return 0

if __name__ == "__main__":
    print('hello')
