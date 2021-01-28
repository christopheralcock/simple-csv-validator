import csv
from io import StringIO


class CsvValidityAssessment:
    """
    Details CSV validty
    """
    def __init__(
        self,
        file_path: 'str',
        expected_column_count: 'int'
    ):
        """
        Construct a new 'CsvValidityAssessment' object.

        :param file_path: The location of the csv in question
        :param expected_column_count: The number of columns we're expecting
            the csv to have
        :return: returns nothing
        """
        self.file_path = file_path
        self.expected_column_count = expected_column_count
        self.csv_is_valid = True
        self.first_problem_row = None
        self.first_problem_row_width = None


def validate_csv_string(
    csv_string: 'str',
    file_path: 'str',
    expected_column_count: 'int',
    delimiter: 'str',
    quotechar: 'str' = '"'
) -> CsvValidityAssessment:
    """
    Take string of csv data and return CsvValidityAssessment

    :param csv_string: A string of csv data
    :param file_path: The location of the csv in question, used here to pass
        through to the CsvValidityAssessment to help action insights
    :param expected_column_count: The number of columns we're expecting
        the csv to have
    :param delimiter: character that separates the line of the csv into
        its columns, typically a comma
    :param quotechar: character that wraps a delimiter when you want to
        use it without it separating a column in two, typically a double
        quotation mark
    :return: returns CsvValidityAssessment
    """
    with StringIO(csv_string) as csv_file:
        return validate_csv(
            csv_file,
            file_path,
            expected_column_count,
            delimiter,
            quotechar)


def validate_csv_file(
    file_path: 'str',
    expected_column_count: 'int',
    delimiter: 'str',
    quotechar: 'str' = '"'
) -> CsvValidityAssessment:
    """
    Take string of csv file location and return CsvValidityAssessment

    :param file_path: The location of the csv in question
    :param expected_column_count: The number of columns we're expecting
        the csv to have
    :param delimiter: character that separates the line of the csv into
        its columns, typically a comma
    :param quotechar: character that wraps a delimiter when you want to
        use it without it separating a column in two, typically a double
        quotation mark
    :return: returns CsvValidityAssessment
    """
    with open(file_path) as csv_file:
        return validate_csv(
            csv_file,
            file_path,
            expected_column_count,
            delimiter,
            quotechar)


def validate_csv(
    csv_file,
    file_path: 'str',
    expected_column_count: 'int',
    delimiter: 'str',
    quotechar: 'str' = '"'
) -> CsvValidityAssessment:
    """
    Take csv file or file-like object and return assessment of its validity

    :param csv_file: A file-like object such as the one returned by the
        open method, or the io.StringIO method
    :param file_path: The location of the csv in question
    :param expected_column_count: The number of columns we're expecting
        the csv to have
    :param delimiter: character that separates the line of the csv into
        its columns, typically a comma
    :param quotechar: character that wraps a delimiter when you want to
        use it without it separating a column in two, typically a double
        quotation mark
    :return: returns CsvValidityAssessment
    """
    assessment = CsvValidityAssessment(file_path, expected_column_count)
    for row in csv.reader(csv_file, delimiter=delimiter, quotechar=quotechar):
        if len(row) != expected_column_count:
            assessment.first_problem_row = row
            assessment.csv_is_valid = False
            assessment.first_problem_row_width = len(row)
            break
    return assessment
