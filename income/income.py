#!/usr/env/bin python3
#coding:utf-8

"""
Income

This module gathers sources of income found on the 1040 and computes AGI and
taxable income. When run as a script, the program will attempt to read from
various forms (1099, W-2, etc.) to automatically gather this information.
"""

# 2441 line 26
def _taxable_dep_care():
    return 0

def _taxable_adoption_benefits():
    return 0

# Line 6b. Use SS worksheet
def _taxable_ss():
    return 0

def totalIncome():
    """
    totalIncome computes the total income (line 9) of the taxpayer:
        - Wages
        - Adoption Benefits
        - Taxable dependent care benefits
        - Taxable Interest
        - Ordinary Dividends
        - IRA Distributions
        - Pension Distributions
        - Taxable Social Security Benefits
        - Capital Gain or Loss
        - Additional Income from Schedule 1
    """
    return 0

# Compute Schedule 1 line 26
def adjustedGrossIncome():
    """
    adjustedGrossIncome computes the AGI (line 11) by subtracting adjustments
    to income from the taxpayer's total income (line 9).
    """
    return 0

def taxableIncome(agi, deduction):
    """
    taxableIncome computes the taxable income (line 15) of the taxpayer. The
    deductions from Schedule A are compared against the standard deduction for
    the given filing status and the greater is chosen automatically.
    """
    return 0

if __name__ == "__main__":
    print('hello')
