#!/usr/bin/env python3
#coding:utf-8

"""
W-2 Generator

This program populates a form W-2 for purposes of practing tax returns. Wages
are generated within the minimum amount to issue (e.g 600) and the threshold
for the highest tax bracket (MFJ)

TODO: Currently this assumes wages are equal to taxable income, which is clearly
wrong. Need to incorporate other packages that properly adjust income to arrive
at TI.
"""

from math import floor
from random import randint

from pypdf import PdfReader, PdfWriter

from figure.tax_schedule import figureTax

writer = PdfWriter()

# Generate random wages between $600 and $751,601
def _rdmWages():
    # Range is multiplied by 100 to produce dollars and cents when dividing
    return randint(600_00, 751600_00) / 100

# Computes SS and Med tax (including additional medicare tax owed)
def _fica(wages):
    ss = min(wages, 176_100) * 0.0620
    medicare = wages * 0.0145 + max(wages - 200_000, 0) * 0.009

    return (ss, medicare)

# keep [places] digits after the decimal point
def _trunc(figure, places=2):
    factor = 10 ** places

    return floor(figure * factor) / factor

# Used only for the unusual states of '/Off' and '/1' in Box 13
def _onoff():
    return '/1' if randint(0, 1) else '/Off'

# Fields are consistent across copies and follow the <parent>.<child> format
# described in the PDF specification.
defaultValues = {
        'BoxA_ReadOrder[0].f2_01[0]': '123-45-6879',                            # Employee SSN
        'Col_Left[0].f2_02[0]': '99-9999918',                                   # EIN
        'Col_Left[0].f2_03[0]': 'BigCorp\n123 Main St,\nAnytown,\nMD 12345',    # Employee Address
        'Col_Left[0].f2_04[0]': 12345,                                          # Control Number
        'Col_Left[0].FirstName_ReadOrder[0].f2_05[0]': 'John',                  # First Name
        'Col_Left[0].LastName_ReadOrder[0].f2_06[0]': 'Taxpayer',               # Last Name
        'Col_Left[0].f2_08[0]': '1 Some Ave,\nAnytown,\nMD, 12345',             # Employee Address
        'Col_Right[0].Box1_ReadOrder[0].f2_09[0]': 100000,                      # Wages
        'Col_Right[0].f2_10[0]': 15000,                                         # Fed W/H
        'Col_Right[0].Box3_ReadOrder[0].f2_11[0]': 100000,                      # Social Security
        'Col_Right[0].f2_12[0]': 6200,                                          # SS W/H
        'Col_Right[0].Box5_ReadOrder[0].f2_13[0]': 100000,                      # Social Security
        'Col_Right[0].f2_14[0]': 1450,                                          # Medicare W/H
        'Col_Right[0].Box7_ReadOrder[0].f2_15[0]': 0,                           # SS Tips
        'Col_Right[0].f2_16[0]': 0,                                             # Allocated Tips
        'Col_Right[0].f2_18[0]': 0,                                             # Dependent Care Benefits
        'Col_Right[0].Line12_ReadOrder[0].f2_20[0]': None,                      # Box 12
        'Col_Right[0].Line12_ReadOrder[0].f2_21[0]': None,
        'Col_Right[0].Line12_ReadOrder[0].f2_22[0]': None,
        'Col_Right[0].Line12_ReadOrder[0].f2_23[0]': None,
        'Col_Right[0].Line12_ReadOrder[0].f2_24[0]': None,
        'Col_Right[0].Line12_ReadOrder[0].f2_25[0]': None,
        'Col_Right[0].Line12_ReadOrder[0].f2_26[0]': None,
        'Col_Right[0].Line12_ReadOrder[0].f2_27[0]': None,
        'Col_Right[0].Statutory_ReadOrder[0].c2_2[0]': '/Off',                  # Box 13
        'Col_Right[0].Retirement_ReadOrder[0].c2_3[0]': '/1',

        'Boxes15_ReadOrder[0].Box15_ReadOrder[0].f2_29[0]': 'MD',               # State
        'Box16_ReadOrder[0].f2_33[0]': 100000,                                  # State Wages
        'Box17_ReadOrder[0].f2_35[0]': 8000,                                    # State Tax
        'Box18_ReadOrder[0].f2_37[0]': 100000,                                  # Local Wages
        'Box19_ReadOrder[0].f2_39[0]': 4000,                                    # Local Tax
        }

# Randomize wages and compute withholding to put on form W-2
def _wage_and_wh():
    wages = _rdmWages()
    fed = _trunc(figureTax(wages))
    ss, med = _fica(wages)

    # TODO: Handle different states
    mdRates = [0.02, 0.03, 0.04, 0.0475, 0.05, 0.0525, 0.055, 0.0575]
    mdSchedule = [1000, 2000, 3000, 100_000, 125_000, 150_000, 250_000]

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

    return {
        'topmostSubform[0].CopyB[0].Col_Right[0].Box1_ReadOrder[0].f2_09[0]': wages,
        'topmostSubform[0].CopyB[0].Col_Right[0].f2_10[0]': fed,
        'topmostSubform[0].CopyB[0].Col_Right[0].Box3_ReadOrder[0].f2_11[0]': wages,
        'topmostSubform[0].CopyB[0].Col_Right[0].f2_12[0]': _trunc(ss),
        'topmostSubform[0].CopyB[0].Col_Right[0].Box5_ReadOrder[0].f2_13[0]': wages,
        'topmostSubform[0].CopyB[0].Col_Right[0].f2_14[0]': _trunc(med),

        'topmostSubform[0].CopyB[0].Box16_ReadOrder[0].f2_33[0]': wages,
        'topmostSubform[0].CopyB[0].Box17_ReadOrder[0].f2_35[0]': _trunc(figureTax(wages, mdtaxtable2025)),
        'topmostSubform[0].CopyB[0].Box18_ReadOrder[0].f2_37[0]': wages,
        'topmostSubform[0].CopyB[0].Box19_ReadOrder[0].f2_39[0]': _trunc(wages * 0.0320),
        }

if __name__ == "__main__":
    reader = PdfReader('forms/fw2.pdf')

    writer.append(reader)

    wage_info = _wage_and_wh()
    values = { f'topmostSubform[0].CopyB[0].{field}': value for field, value in defaultValues.items() } | wage_info
    values['topmostSubform[0].CopyB[0].Col_Right[0].Retirement_ReadOrder[0].c2_3[0]'] = _onoff()

    writer.update_page_form_field_values(None, values, auto_regenerate=False)

    with open('filled-w-2.pdf', 'wb') as output:
        writer.write(output)
