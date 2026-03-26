import sys
from src.dsproject.logger import logger

def error_message_detail(error, error_detail):
    _, _, exc_tb = error_detail
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"""
    Error occurred in file: {file_name}
    Line number: {exc_tb.tb_lineno}
    Error message: {str(error)}
"""
    return error_message


class CustomException(Exception):
    def __init__(self, error, error_detail):
        super().__init__(str(error))
        self.error_message = error_message_detail(error, error_detail)

    def __str__(self):
        return self.error_message