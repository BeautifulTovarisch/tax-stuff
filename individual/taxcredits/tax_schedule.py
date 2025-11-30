#!/usr/bin/env python3

"""
Tax Schedule

This program computes the tax on taxable income given a tax rate schedule. The
schedule is defined as an associative list of the following tuples:

    (upperbound: marginalRate)

where `upperBound` is upper limit for income taxed at the `marginalRate` for a
given bracket.

NOTE: This program is only suitable for computing income subject to a tax rate
schedule, and will not compute overall tax correctly for other taxable income
such as capital gains.
"""

import math

# Upper bounds defining each tax bracket for 2025
schedule2025 = [11925,
                48475,
                103350,
                197300,
                250525,
                626350]

fedRates = [0.10, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37]

# TODO. This table should be easy to compute given the brackets and rates
taxtable2025 = {
        0: lambda i: i * 0.10,
        11_925: lambda i: 1192.50 + ((i - 11_925) * 0.12),
        48_475: lambda i: 5578.50 + ((i - 48_475) * 0.22),
        103_350: lambda i: 17651.00 + ((i - 103_350) * 0.24),
        197_300: lambda i: 40199.00 + ((i - 197_300) * 0.32),
        250_525: lambda i: 57231.00 + ((i - 250_525) * 0.35),
        626_350: lambda i: 188769.75 + ((i - 626_350) * 0.37)
        }

mdtaxtable2025 = {
        0: lambda i: i * 0.02,
        1000: lambda i: 20 + ((i - 1000) * 0.03),
        2000: lambda i: 50 + ((i - 2000) * 0.04),
        3000: lambda i: 90 + ((i - 3000) * 0.0475),
        100_000: lambda i: 4697.50 + ((i - 100_000) * 0.05),
        125_000: lambda i: 5947.50 + ((i - 125_000) * 0.0525),
        150_000: lambda i: 7260.00 + ((i - 150_000) * 0.0550),
        250_000: lambda i: 12760.00 + ((i - 250_000) * 0.0575)
        }

def _compute_tax_schedule(schedule, rates):
    return {}

# Straightforward implementation used for testing. Works for all taxable income.
def _oracle(income, schedule=schedule2025, rates=fedRates):
    if income < 0:
        raise ValueError('income must be nonnegative')

    if len(schedule) > len(rates):
        raise ValueError('bracket boundaries may not exceed number of tax brackets')

    if not schedule:
        return 0.0

    # If the schedule isn't sorted, the income bounds will be completely wrong
    sched = sorted(schedule)

    brackets = [sched[0]] + [sched[i] - sched[i-1] for i in range(1, len(sched))]

    tax = 0.0
    for (bracket, rate) in zip(brackets, rates):
        taxedIncome = max(min(income, bracket), 0.0)
        tax += taxedIncome * rate

        income -= taxedIncome

    # Handle the final tax bracket, if any income is left over.
    return tax + (income * rates[-1])

# Compute tax using lookup tables and a formula. Consistent with how actual tax
# preparers would compute tax for taxable income over $100,000. The keys in the
# taxtable represent the brackets, and the corresponding value computes the tax
# according to the formula found in the instructions for the 1040.
def _tax_schedule(income, taxtable=taxtable2025):
    bracket = 0.0
    for k in taxtable:
        # Supremum
        if income > k:
            bracket = max(bracket, k)

    return taxtable[bracket](income)

def figureTax(income, taxtable=taxtable2025):
    """
    figureTax computes the tax on `income` by applying the `schedule`.

    Input:
        income (float): Total taxable income

        schedule (List(tuple)): A tax schedule whose keys define the bounds of the bracket
        and whose values indicate the marginal tax rate of that bracket.

    Output:
        The tax on the provided income.

    Raises:
        - ValueError if income is negative

    >>> figureTax(0, [])
    0.0

    >>> figureTax(0, [11925])
    0.0

    >>> figureTax(11926, schedule2025)
    1192.62

    >>> figureTax(147790, schedule2025)
    28316.6

    >>> round(figureTax(139819, [11600, 47150, 100525, 191950, 243735]), 2)
    26599.06

    >>> figureTax(12345, [1, 2, 3, 4, 5, 6, 7, 8])
    Traceback (most recent call last):
        ...
    ValueError: bracket boundaries may not exceed number of tax brackets

    >>> figureTax(-1, [11925])
    Traceback (most recent call last):
        ...
    ValueError: income must be nonnegative
    """

    return _tax_schedule(income, taxtable)

if __name__ == "__main__":
    income = input('Please enter your taxable income: ')

    mdRates = [0.02, 0.03, 0.04, 0.0475, 0.05, 0.0525, 0.055, 0.0575]
    mdSchedule = [1000, 2000, 3000, 100_000, 125_000, 150_000, 250_000]

    print(f'federal\t {figureTax(float(income)):20}')
    print(f'state\t {figureTax(float(income), mdtaxtable2025):20}')
    print(f'local\t {(float(income) * 0.0320):20}')
