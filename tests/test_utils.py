# -*- coding: utf-8 -*-

"""
Tests the utilities of the application.
"""
from datetime import datetime

from pytest import fixture, raises

from stackstatistics.utils import APIRequest, ResultDictionaryFactory
from stackstatistics.constants import API_SUCCESS_CODE_RESPONSE


@fixture
def valid_input_arguments():
    return {'since': datetime(2017, 6, 9, 10, 0), 'until': datetime(2017, 6, 10, 12, 2), 'output_format': 'json'}


@fixture
def invalid_number_input_arguments():
    return {'until': datetime(2017, 8, 10, 12, 0), 'output_format': 'json'}


@fixture
def invalid_input_arguments():
    return {'since': "2017", 'until': datetime(2017, 8, 10, 12, 0), 'output_format': 'json'}


@fixture
def response_keys():
    return ['items', 'has_more', 'quota_max', 'quota_remaining']


@fixture
def response_item_array_keys():
    return ['owner', 'is_accepted', 'score', 'last_activity_date',
            'last_edit_date', 'creation_date', 'answer_id', 'question_id']


@fixture
def valid_answer_ids_list():
    return [44456952, 44471411, 44466436]


@fixture
def error_response_keys():
    return ['error_id', 'error_message', 'error_name']


@fixture
def result_dictionary_keys():
    return ['total_accepted_answers', 'accepted_answers_average_score',
            'average_answers_per_question', 'top_ten_answers_comment_count']


@fixture
def answers_per_question():
    return {44461571: 1, 43619845: 1, 44456977: 2}


@fixture
def comments_per_answer():
    return {44453729: 1, 44466436: 3}


def test_api_request_answers_retrieval(response_keys, response_item_array_keys, valid_input_arguments):
    """ Tests the retrieve_answers function of APIRequest class. """
    api_request_instance = APIRequest(valid_input_arguments)
    answers_response = api_request_instance.retrieve_answers()
    status_code = answers_response.status_code
    answers_response_json = answers_response.json()

    assert isinstance(status_code, int)
    assert isinstance(answers_response_json, dict)

    assert status_code == API_SUCCESS_CODE_RESPONSE, "The response code should be 200 for success"
    # Ensure the JSON response includes the expected fields.
    assert set(response_keys).issubset(answers_response_json.keys()), "The response_keys should be in the response"

    # Assure the 'items' JSON field has as a value a JSON array.
    answers_response_json_items = answers_response_json['items']
    assert isinstance(answers_response_json_items, list)
    # Ensure the JSON objects in the 'items' array, have the expected fields.
    assert set(response_item_array_keys).issubset(answers_response_json_items[0].keys()), \
        "The response_array_keys should be in the objects of the item array (1st element check)"


def test_api_request_comments_retrieval(response_keys, valid_input_arguments,
                                        error_response_keys, valid_answer_ids_list):
    """ Tests the retrieve_comments function of APIRequest class with valid and invalid inputs. """
    # Retrieve comments with valid input arguments.
    api_request_instance = APIRequest(valid_input_arguments)
    comments_response = api_request_instance.retrieve_comments(valid_answer_ids_list)
    status_code = comments_response.status_code
    comments_response_json = comments_response.json()

    assert isinstance(status_code, int)
    assert isinstance(comments_response_json, dict)

    assert status_code == API_SUCCESS_CODE_RESPONSE, "The response code should be 200 for success"
    assert set(response_keys).issubset(comments_response_json.keys()), "The response_keys should be in the response"

    # Retrieve comments with invalid input arguments.
    invalid_answer_ids_list = []
    comments_response_error = api_request_instance.retrieve_comments(invalid_answer_ids_list)
    comments_response_error_json = comments_response_error.json()
    assert isinstance(comments_response_error_json, dict)
    assert set(error_response_keys).issubset(
        comments_response_error_json.keys()), "The error_response_keys should be in the response"
    assert comments_response_error.status_code != API_SUCCESS_CODE_RESPONSE, "The response code should not be 200"


def test_api_request_with_invalid_arguments(invalid_input_arguments, invalid_number_input_arguments):
    """ Tests the APIRequest class with invalid input arguments. """
    # omit one required parameter
    with raises(KeyError):
        APIRequest(invalid_number_input_arguments)

    # test the _datetime_to_timestamp function
    api_request_instance = APIRequest(invalid_input_arguments)
    with raises(AttributeError):
        api_request_instance.retrieve_answers()


def test_result_dictionary_factory_class(result_dictionary_keys, answers_per_question, comments_per_answer):
    """ Tests the ResultDictionaryFactory class. """
    # Set up a fixed list and calculate its mean value.
    accepted_answers_score_list = [4, 3, 4, 5]
    mean_value = 4

    # Set up the rest arguments of create function
    number_of_answers_per_question = answers_per_question
    number_of_comments_per_answer = comments_per_answer

    result_dictionary = ResultDictionaryFactory().create(
        accepted_answers_score_list, number_of_answers_per_question.values(), number_of_comments_per_answer)

    assert isinstance(result_dictionary, dict)
    assert set(result_dictionary_keys).issubset(
        result_dictionary.keys()), "The result_dictionary_keys should be in the result"

    # test the mean function
    mean_value_of_accepted_answers_score_list = ResultDictionaryFactory.mean(accepted_answers_score_list)
    assert mean_value_of_accepted_answers_score_list == mean_value
