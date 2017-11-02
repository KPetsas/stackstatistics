# -*- coding: utf-8 -*-

"""
Tests the validations of the application.
"""
from datetime import datetime
from argparse import ArgumentTypeError

from pytest import fixture, raises

from stackstatistics.validations import valid_date_is


@fixture
def valid_input_date():
    return "2017-6-11 10:00:00"


@fixture
def invalid_input_date():
    return "2017/6/11-10:00:00"


def test_valid_date_is(valid_input_date, invalid_input_date):
    """ Tests the valid_date_is function for valid and invalid input. """
    assert isinstance(valid_date_is(valid_input_date), datetime)

    # Ensure that invalid input raises the related error.
    with raises(ArgumentTypeError):
        valid_date_is(invalid_input_date)
