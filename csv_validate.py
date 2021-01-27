import csv

class CsvValidityAssessment:
    """
    Details CSV validty
    """
    def __init__(self, file_path, expected_column_count):
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


def validate_csv(
    file_path:'str',
    expected_column_count:'int',
    delimiter:'char',
    quotechar:'char'='"') -> CsvValidityAssessment:
    """
        Take details of csv and return assessment of its validity

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
    with open(file_path) as csvfile:
        for row in csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar):
            if len(row) != expected_column_count:
                assessment.first_problem_row = row
                assessment.csv_is_valid = False
                assessment.first_problem_row_width = len(row)
                break
    return assessment
