import pytest
from csv_validate import validate_csv

def test_simple_valid_csv():
    assert validate_csv("./test_data/simple_valid.csv",3,',').csv_is_valid == True

def test_non_quadralateral_invalid_csv():
    assert validate_csv("./test_data/non_quadralateral_invalid.csv",2,',').csv_is_valid == False

def test_complex_escaping_valid_csv():
    assert validate_csv("./test_data/complex_escaping_valid.csv",3,',').csv_is_valid

def test_complex_escaping_valid_csv_with_wrong_delimiter():
    assert validate_csv("./test_data/complex_escaping_valid.csv",3,'|').csv_is_valid == False

def test_quotes_strings_valid_csv():
    assert validate_csv("./test_data/quotes_strings_valid.csv",3,',').csv_is_valid == True

