import csv
from azure.storage.blob import BlobServiceClient
from io import BytesIO, StringIO
from os import remove


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

    def express_as_text(self):
        if self.csv_is_valid:
            assessment = f"{self.file_path} is valid csv"
        else:
            assessment = f"""{self.file_path} is invalid. \
expected {self.expected_column_count} columns \
but found {self.first_problem_row_width} \
in this row: {self.first_problem_row}"""
        return assessment


def validate_csv_from_azure_blob_storage(
    file_name: 'str',
    container_name: 'str',
    connection_string: 'str',
    expected_column_count: 'int',
    delimiter: 'str',
    quotechar: 'str' = '"',
    temp_file_path: 'str' = 'temp.csv',
) -> CsvValidityAssessment:
    """
    Take azure blob storage details of csv and return CsvValidityAssessment

    :param file_name: The name of the file on Azure
    :param container_namme: The name of the Azure container
    :param connection_string: The Azure connection string. e.g.
        "DefaultEndpointsProtocol=https;AccountName=xxx;\
        AccountKey=xxx/xxx+xxx==;EndpointSuffix=core.windows.net"
    :param expected_column_count: The number of columns we're expecting
        the csv to have
    :param delimiter: character that separates the line of the csv into
        its columns, typically a comma
    :param quotechar: character that wraps a delimiter when you want to
        use it without it separating a column in two, typically a double
        quotation mark
    :param temp_file_path: The path for it to save the temporary file
    :return: returns CsvValidityAssessment
    """
    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(file_name)
    streamdownloader = blob_client.download_blob()
    stream = BytesIO()
    streamdownloader.readinto(stream)
    with open(temp_file_path, 'wb') as csv_file:
        csv_file.write(stream.getbuffer())
    with open(temp_file_path, 'r') as csv_file:
        assessment = validate_csv(
            csv_file,
            f"{container_name}: {file_name}",
            expected_column_count,
            delimiter)
    remove(temp_file_path)
    return assessment


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
