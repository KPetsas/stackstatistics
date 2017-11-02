#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains all the validations needed for the stackstatistics package.
"""
from datetime import datetime
from argparse import ArgumentTypeError


def valid_date_is(input_date):
    """ Validates that the user input date/time has a specific format.

    :param (str) input_date: A string, the date/time user input.
    :returns: datetime.
    """
    try:
        return datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        msg = "Invalid input date: {0}".format(input_date)
        raise ArgumentTypeError(msg)
