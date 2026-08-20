import pytest
from project import validate_date, book_search, time_reading
from unittest.mock import patch


def test_validate_date():
    assert validate_date("09/08/2026") == "09/08/2026"
    assert validate_date("09-08-2026") == "09/08/2026"
    assert validate_date("09.08.2026") == "09/08/2026"
    assert validate_date("August 9, 2026") == None
    assert validate_date("Banana") == None

@patch("project.requests.get")
def test_book_search_true(mock_book_search):
    mock_book_search.return_value.json.return_value = {"docs": [1]}
    result = book_search("tolkien", "the+hobbit")
    assert result == True


@patch("project.requests.get")
def test_book_search_false(mock_book_search):
    mock_book_search.return_value.json.return_value = {"docs": []}
    result = book_search("tolkien", "the+hobbit")
    assert result == False


def test_time_reading():
    #normal case
    assert time_reading("18/08/2026", "10/08/2026") == "8 days"
    #end befor begin
    assert time_reading("10/08/2026", "18/08/2026") == "-"
    # same dates
    assert time_reading("10/08/2026", "10/08/2026") == "0 days"
    # invalid date
    assert time_reading("10/16/2026", "40/80/2026") == "ValueError"
    assert time_reading("14.12.2026", "23.08.2027") == "ValueError"




