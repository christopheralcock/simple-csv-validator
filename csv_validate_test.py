from csv_validate import validate_csv_file, validate_csv_string


def test_simple_valid_csv():
    assert validate_csv_file(
        "./test_data/simple_valid.csv",
        3,
        ','
    ).csv_is_valid is True


def test_simple_valid_csv_from_string():
    csv_string = """Col1,Col2,Col3
val1,val2,val3
val4,val5,val6
val7,val8,val9"""
    assert validate_csv_string(
        csv_string,
        "simple_valid.csv",
        3,
        ','
    ).csv_is_valid is True


def test_non_quadralateral_invalid_csv():
    assert validate_csv_file(
        "./test_data/non_quadralateral_invalid.csv",
        2,
        ','
    ).csv_is_valid is False


def test_complex_escaping_valid_csv():
    assert validate_csv_file(
        "./test_data/complex_escaping_valid.csv",
        3,
        ','
    ).csv_is_valid is True


def test_complex_escaping_valid_csv_with_wrong_delimiter():
    assert validate_csv_file(
        "./test_data/complex_escaping_valid.csv",
        3,
        '|'
    ).csv_is_valid is False


def test_quotes_strings_valid_csv():
    assert validate_csv_file(
        "./test_data/quotes_strings_valid.csv",
        3,
        ','
    ).csv_is_valid is True
