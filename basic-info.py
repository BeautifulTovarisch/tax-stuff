#!/usr/bin/env python3
#coding:utf-8

"""
1040 Generator

This program populates a 1040 with basic information about a taxpayer including:

    - Name
    - Address
    - SSN
    - Dependents
    - Filing Status

The resulting 1040 is intended to be used by other programs which compute the
income, tax, credits and payments, and tax liability of the tax payer. In
particular, the filing status of the taxpayer is needed in order to accurately
compute withholding information for other form generators etc.
"""

from math import floor
from enum import Enum
from random import randint

from pypdf import PdfReader, PdfWriter

writer = PdfWriter()

def _onoff():
    return '/1' if randint(0, 1) else '/Off'

def _filing_status(status=None):
    # This strange format is an artifact of the unusual form input for Filing Status
    # checkboxes on the 1040
    filingStatus = [
            ('topmostSubform[0].Page1[0].FilingStatus_ReadOrder[0].c1_3[0]', '/1'),   # S /1
            ('topmostSubform[0].Page1[0].c1_3[0]', '/2'),                             # HOH /2
            ('topmostSubform[0].Page1[0].FilingStatus_ReadOrder[0].c1_3[1]', '/3'),   # MFJ /3
            ('topmostSubform[0].Page1[0].FilingStatus_ReadOrder[0].c1_3[2]', '/4'),   # MFS /4
            ('topmostSubform[0].Page1[0].c1_3[1]', '/5'),                             # QSS /5
            ]

    return filingStatus[status or randint(0, 4)]

# Selects between 0 and 3 dependents. Whether the dependent is used for the CTC
# or ODC is static
def _dependents(numDeps=0):
    dependents = [
            {'topmostSubform[0].Page1[0].Table_Dependents[0].Row1[0].f1_20[0]': 'Jake Taxpayer',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row1[0].f1_21[0]': '123-45-6791',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row1[0].f1_22[0]': 'Child',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row1[0].c1_14[0]': '/1',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row1[0].c1_15[0]': ''},

            {'topmostSubform[0].Page1[0].Table_Dependents[0].Row2[0].f1_23[0]': 'Jacquelyn Taxpayer',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row2[0].f1_24[0]': '123-45-6792',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row2[0].f1_25[0]': 'Child',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row2[0].c1_16[0]': '',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row2[0].c1_17[0]': '/1'},

            { 'topmostSubform[0].Page1[0].Table_Dependents[0].Row3[0]': '',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row3[0].f1_26[0]': 'Jessie Taxpayer',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row3[0].f1_27[0]': '123-45-6793',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row3[0].f1_28[0]': 'Child',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row3[0].c1_18[0]': '/1',
             'topmostSubform[0].Page1[0].Table_Dependents[0].Row3[0].c1_19[0]': ''}
            ]

    dict = {}
    deps = dependents[0:(numDeps or randint(0, 3))]

    for d in deps:
        dict |= d

    return dict

def _spouse():
    return {
        'topmostSubform[0].Page1[0].f1_07[0]': 'Jane',
        'topmostSubform[0].Page1[0].f1_08[0]': 'Taxpayer',
        'topmostSubform[0].Page1[0].f1_09[0]': '123-45-6790',
        'topmostSubform[0].Page1[0].c1_11[0]': _onoff(),    # > 65 Spouse
        'topmostSubform[0].Page1[0].c1_12[0]': _onoff(),    # Blind Spouse
        'topmostSubform[0].Page1[0].c1_2[0]': _onoff(),     # Election Campaign Spouse
        }

# For certain filing statuses, additional information about the spouse and/or
# any qualifying dependents must be entered.
def _additional_info(filingStatus):
    return {
            '/1': {},
            '/2': _dependents(randint(1, 3)),
            '/3': _spouse(),
            '/4': { 'topmostSubform[0].Page1[0].f1_18[0]': 'Jane Taxpayer' },
            '/5': _dependents(randint(1, 3)),
            }[filingStatus]


# Fields are consistent across copies and follow the <parent>.<child> format
# described in the PDF specification.
defaultValues = {
        'topmostSubform[0].Page1[0].f1_04[0]': 'John',          # First Name
        'topmostSubform[0].Page1[0].f1_05[0]': 'Taxpayer',      # Last Name
        'topmostSubform[0].Page1[0].f1_06[0]': '123-45-6789',   # SSN
        'topmostSubform[0].Page1[0].f1_07[0]': '',              # Spouse First Name
        'topmostSubform[0].Page1[0].f1_08[0]': '',              # Spouse Last Name
        'topmostSubform[0].Page1[0].f1_09[0]': '',              # Spouse SSN

        'topmostSubform[0].Page1[0].Address_ReadOrder[0].f1_10[0]': '1 Some Avenue',    # Street
        'topmostSubform[0].Page1[0].Address_ReadOrder[0].f1_11[0]': '',                 # APT
        'topmostSubform[0].Page1[0].Address_ReadOrder[0].f1_12[0]': 'Anytown',          # City/Town
        'topmostSubform[0].Page1[0].Address_ReadOrder[0].f1_13[0]': 'MD',               # State
        'topmostSubform[0].Page1[0].Address_ReadOrder[0].f1_14[0]': '12345',            # Zipcode

        'topmostSubform[0].Page1[0].c1_1[0]': '/Off', # Election Campaign
        'topmostSubform[0].Page1[0].c1_2[0]': '', # Election Campaign Spouse

        # Filing Status
        'topmostSubform[0].Page1[0].FilingStatus_ReadOrder[0].c1_3[0]': '',   # S /1
        'topmostSubform[0].Page1[0].c1_3[0]': '',                             # HOH /2
        'topmostSubform[0].Page1[0].FilingStatus_ReadOrder[0].c1_3[1]': '',   # MFJ /3
        'topmostSubform[0].Page1[0].FilingStatus_ReadOrder[0].c1_3[2]': '',   # MFS /4
        'topmostSubform[0].Page1[0].c1_3[1]': '',                             # QSS /5
        'topmostSubform[0].Page1[0].f1_18[0]': '',                            # MFS Spouse

        'topmostSubform[0].Page1[0].c1_5[0]': '',   # Crypto Yes
        'topmostSubform[0].Page1[0].c1_5[1]': '/2', # Crypto No

        'topmostSubform[0].Page1[0].c1_9[0]': '',   # > 65
        'topmostSubform[0].Page1[0].c1_10[0]': '',  # Blind
    }

if __name__ == "__main__":
    reader = PdfReader('forms/f1040.pdf')

    (field, value) = _filing_status()

    defaultValues[field] = value

    defaultValues |= _dependents()
    defaultValues |= _additional_info(value)

    writer.append(reader)
    writer.update_page_form_field_values(None, defaultValues, auto_regenerate=False)

    with open('filled-1040.pdf', 'wb') as output:
        writer.write(output)
