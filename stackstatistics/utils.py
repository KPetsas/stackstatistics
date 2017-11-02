#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Includes all the utilities for the application.
"""

import requests
import time
import json

from tabulate import tabulate
from flask_table import Table, Col

import constants


class APIRequest(object):
    """ StackExchange API Request functions and related utilities.

    :param (dict) options: A dictionary, the user input options.
    """
    def __init__(self, options):
        """ Return an APIRequest object with the date/time range specified. """
        self.since = options['since']
        self.until = options['until']

    def retrieve_answers(self):
        """ Request to retrieve answers from the corresponding api endpoint. """
        return requests.get('{0}{1}{2}{3}{4}{5}{6}'
                            .format(constants.API_URI_SCHEME_AUTHORITY,
                                    constants.API_URI_ANSWERS_PATH,
                                    constants.API_URI_ANSWERS_COMMON_QUERY,
                                    constants.API_URI_ANSWERS_SINCE_QUERY,
                                    APIRequest._datetime_to_timestamp(self.since),
                                    constants.API_URI_ANSWERS_UNTIL_QUERY,
                                    APIRequest._datetime_to_timestamp(self.until)))

    @staticmethod
    def retrieve_comments(answer_ids):
        """ Request to retrieve the comments for the specified answer ids.

        :param (list) answer_ids: An array with the selected answer ids.
        :returns: Response model.
        """
        return requests.get('{0}{1}/{2}{3}{4}'
                            .format(constants.API_URI_SCHEME_AUTHORITY,
                                    constants.API_URI_ANSWERS_PATH,
                                    ';'.join(str(answer_id) for answer_id in answer_ids),
                                    constants.API_URI_COMMENTS_PATH,
                                    constants.API_URI_ANSWERS_COMMON_QUERY))

    @staticmethod
    def _datetime_to_timestamp(input_date):
        """ Simple datetime to timestamp converter. """
        return int(time.mktime(input_date.timetuple()))


class ResultDictionaryFactory(object):
    """ Creates a dictionary that includes the data analytics for the specified date/time. """

    def create(self, accepted_answers_score_list, number_of_answers_per_question, number_of_comments_per_answer):
        """ Create and return a dictionary with the results.

        :param (list) accepted_answers_score_list: A list with the accepted answers score.
        :param (list) number_of_answers_per_question: A list with the number of answers per question.
        :param (dict) number_of_comments_per_answer: A dictionary with the number of comments per question.
        :returns: The result dictionary.
        """
        result_dict = dict()
        result_dict['total_accepted_answers'] = len(accepted_answers_score_list)
        result_dict['accepted_answers_average_score'] = round(self.mean(accepted_answers_score_list), 2)
        result_dict['average_answers_per_question'] = round(self.mean(number_of_answers_per_question), 2)
        result_dict['top_ten_answers_comment_count'] = number_of_comments_per_answer
        return result_dict

    @staticmethod
    def mean(array):
        """ Return the average of a list. """
        return sum(array)/float(len(array))


class PrintOption(object):
    """ Available print options for the stackstatistics application.

    :param (dict) result_dict: A dictionary, the result of the
                                stackstatistics data retrieval and analysis.
    """
    def __init__(self, result_dict):
        """ Return a PrintOption object whose result dictionary is defined as result_dict. """
        self.result_dict = result_dict

    def json(self, indent=4):
        """ Print to the console the result dictionary, in JSON format.

        :param (int) indent: An optional integer parameter defining
                              the JSON elements indent.
        """
        print json.dumps(self.result_dict, indent=indent)

    def tabular(self, comments_per_answer):
        """ Print to the console the result dictionary, in tabular format.

        :param (list) comments_per_answer: A list of tuples, the number of comments per answer, ready to
                                            be inserted in the tabulate function, in order to create a sub-table.
        """
        # Create an array of tuples to insert into the tabulate function.
        tabulate_data = [(key, value)
                         if key is not 'top_ten_answers_comment_count'
                         else (key, tabulate(comments_per_answer, headers=['answer_id', 'comment_count']))
                         for key, value in self.result_dict.items()]
        print tabulate(tabulate_data, headers=['Statistics', 'Values'])

    def html(self, comments_per_answer_items):
        """ Print to the console the result dictionary, in HTML format.

        :param (list) comments_per_answer_items: A list of Item object instances, the number of comments per answer
         as Item instances, so as to be handled by the _ItemSubTable class, in order to create an HTML sub-table.
        """
        # Create an array of Item instances to be handled by the _ItemTable class.
        items = [Item(key, value)
                 if key is not 'top_ten_answers_comment_count'
                 else (Item(key, _ItemSubTable(comments_per_answer_items)))
                 for key, value in self.result_dict.items()]
        table = _ItemTable(items)
        print(table.__html__())


class Item(object):
    """ A flask table Item.

    :param (str) name: A string, the value of the first column of the table.
    :param description: A number (int or float) or a Table object, the value of the second column of the table.
    """
    def __init__(self, name, description):
        """ Return an Item object whose name is *name* and description is *description*. """
        self.name = name
        self.description = description


class _ItemTable(Table):
    """ Inherit from the Table class and specify the table headers. """
    name = Col('Statistics')
    description = Col('Values')


class _ItemSubTable(Table):
    """ Inherit from the Table class and specify the table headers. """
    name = Col('answer_id')
    description = Col('comment_count')
