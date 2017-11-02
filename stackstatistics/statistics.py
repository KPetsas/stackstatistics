#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The main functionality of the stackstatistics application.
"""
import logging
from sys import argv
from argparse import ArgumentParser
from collections import defaultdict

import constants
import validations
from utils import APIRequest, Item, ResultDictionaryFactory, PrintOption
from __version__ import __version__


def main():
    """ Entry point of stackstatistics package. Parses the user input as date/time range
    and retrieves/analyzes the StackOverflow answer and comment data for the
    given date/time range.
    """
    # Configure the logging level and format
    _logger_set_up()

    # Set up the parser
    statistics_parser = ArgumentParser(description='Retrieve and analyze StackOverflow data.')
    statistics_parser.add_argument("-V", "--version", action='version', version=('stackstatistics %s' % __version__))
    statistics_parser.add_argument("--since", metavar='"YYYY-MM-DD H:M:S"',
                              help='specify the start date/time', required=True, type=validations.valid_date_is)
    statistics_parser.add_argument("--until", metavar='"YYYY-MM-DD H:M:S"',
                              help='specify the end date/time', required=True, type=validations.valid_date_is)
    statistics_parser.add_argument("--output-format", default='tabular', choices=['tabular', 'html', 'json'],
                              type=str.lower, help='specify the output format')

    if len(argv) > 1:
        # Put the given arguments in a dictionary
        options = vars(statistics_parser.parse_args(argv[1:]))

        # validate date arguments order
        if options['since'] > options['until']:
            logging.error('--since argument date/time cannot be greater than --until\'s')
            exit(constants.ERROR_DATE_ARGUMENTS_ORDER)

        # Create an APIRequest object to retrieve data from the StackExchange API
        api_request_object = APIRequest(options)

        logging.info('Retrieving answer data...')
        answers_api_response = api_request_object.retrieve_answers()
        # Get the retrieved json object
        answers_api_response_json = answers_api_response.json()
        # API Response Error Handling
        _verify_api_response(answers_api_response.status_code, answers_api_response_json)

        answer_json_items = answers_api_response_json['items']
        # Retrieve all the answer IDs
        answer_ids_list = list(map(lambda selected_item: selected_item['answer_id'], answer_json_items))

        # Retrieve the score of each accepted answer in a list
        accepted_answers_score_list = [item['score'] for item in answer_json_items if item['is_accepted']]

        # Retrieve the number of answers per question
        number_of_answers_per_question = defaultdict(int)  # default value of int is 0
        for item in answer_json_items:
            number_of_answers_per_question[item['question_id']] += 1

        logging.info('Retrieving comment data...')
        comments_api_response = api_request_object.retrieve_comments(answer_ids_list)
        # Get the retrieved json object
        comments_api_response_json = comments_api_response.json()
        # API Response Error Handling
        _verify_api_response(comments_api_response.status_code, comments_api_response_json)

        # Find the number of comments for each of the 10 answers with the highest score.
        top_ten_answers = set(answer_ids_list[:10])  # lookup in a set is faster
        number_of_comments_per_answer = dict(zip(answer_ids_list[:10], [0] * 10))

        for comments in comments_api_response_json['items']:
            if comments['post_id'] in top_ten_answers:
                number_of_comments_per_answer[comments['post_id']] += 1

        # Pack the results into a dictionary.
        result_dictionary = ResultDictionaryFactory().create(
            accepted_answers_score_list, number_of_answers_per_question.values(), number_of_comments_per_answer)

        # Create an instance of the PrintOption class.
        print_option = PrintOption(result_dictionary)

        if options['output_format'] == 'json':
            print_option.json()
        elif options['output_format'] == 'html':
            # Create an array of Item instances to insert into the html function.
            comments_per_answer_items = [Item(answer_id, comment_count)
                                         for answer_id, comment_count in number_of_comments_per_answer.items()]
            print_option.html(comments_per_answer_items)
        else:
            # Create an array of tuples to insert into the tabular function.
            comments_per_answer = [(answer_id, comment_count)
                                   for answer_id, comment_count in number_of_comments_per_answer.items()]
            print_option.tabular(comments_per_answer)
    else:
        logging.error('No arguments were given.')
        statistics_parser.parse_args(' -h'.split())
        exit(constants.ERROR_NO_ARGUMENTS)


def _logger_set_up(level=logging.INFO):
    """ Logger set-up. Default level is INFO. """
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        level=level, datefmt='%Y-%m-%d %H:%M:%S')


def _verify_api_response(status_code, api_response_json):
    """ Verify that the response has retrieved successfully, else exit the application. """
    if status_code is not constants.API_SUCCESS_CODE_RESPONSE:
        logging.error('Status code: {0}. Reason: {1}: {2}'
                      .format(status_code,
                              api_response_json['error_message'],
                              api_response_json['error_name']))
        exit(constants.ERROR_API_RESPONSE)


if __name__ == "__main__":
    main()
