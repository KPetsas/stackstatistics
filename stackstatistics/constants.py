#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains the constants of the stackstatistics application package.
"""

ERROR_NO_ARGUMENTS = -1
ERROR_DATE_ARGUMENTS_ORDER = -2
ERROR_API_RESPONSE = -3

API_URI_SCHEME_AUTHORITY = "https://api.stackexchange.com"
API_URI_ANSWERS_PATH = "/2.2/answers"
API_URI_ANSWERS_COMMON_QUERY = "?order=desc&sort=votes&site=stackoverflow&pagesize=100"
API_URI_ANSWERS_SINCE_QUERY = "&fromdate="
API_URI_ANSWERS_UNTIL_QUERY = "&todate="
API_URI_COMMENTS_PATH = "/comments"

API_SUCCESS_CODE_RESPONSE = 200
