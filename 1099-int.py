#!/usr/bin/env python3
#coding:utf-8

"""
1099 Generator

This program populates a form 1099 for purposes of practing tax returns. Both
taxable and tax-exempt interest can potentially be reported.
"""

from math import floor
from random import randint

from pypdf import PdfReader, PdfWriter

writer = PdfWriter()

# Generate random amount of interest
def _rdmInt():
    # TODO: Determine some reasonable range for this
    return randint(0, 1_000_000) / 100

# Fields are consistent across copies and follow the <parent>.<child> format
# described in the PDF specification.
defaultValues = {
        'LeftColumn[0].f2_1[0]': 'Bank Co\n123 Main St\nAnytown, MD 12345',     # Payer's Address
        'LeftColumn[0].f2_2[0]': '12-3456789',                                  # Payer's TIN
        'LeftColumn[0].f2_3[0]': '123-45-6789',                                 # Recipients's TIN
        'LeftColumn[0].f2_4[0]': 'John Taxpayer',                               # Recipient's Name
        'LeftColumn[0].f2_5[0]': '1 Some Ave',                                  # Recipient Street
        'LeftColumn[0].f2_6[0]': 'Anytown, MD, 12345',                          # Recipient Town, State, Zip
        'RghtColumn[0].Box1[0].f2_9[0]': 0.00,                                  # Interest Income
        'RghtColumn[0].Box8[0].f2_16[0]': 0.00,                                 # Tax-exempt Interest
    }

if __name__ == "__main__":
    reader = PdfReader('forms/f1099int.pdf')

    values = { f'topmostSubform[0].CopyB[0].{field}': value for field, value in defaultValues.items() }
    values['topmostSubform[0].CopyB[0].RghtColumn[0].Box1[0].f2_9[0]'] = _rdmInt()
    values['topmostSubform[0].CopyB[0].RghtColumn[0].Box8[0].f2_16[0]'] = _rdmInt()

    writer.append(reader)
    writer.update_page_form_field_values(None, values, auto_regenerate=False)

    with open('filled-1099int.pdf', 'wb') as output:
        writer.write(output)
