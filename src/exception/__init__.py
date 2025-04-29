import sys
import logging
import types # Import the types module


def error_message_detail(error: Exception, error_detail: types.ModuleType) -> str: # Use types.ModuleType
    """
    Extracts detailed error information including file name, line number, and the error message.

    :param error: The exception that occurred.
    :param error_detail: The sys module to access traceback details.
    :return: A formatted error message string.
    """
    # Extract traceback details (exception information)
    _, _, exc_tb = error_detail.exc_info()

    # Check if traceback exists
    if exc_tb is None:
        # Handle cases where no exception is being processed or traceback is unavailable
        error_message = f"Error occurred: {str(error)} (Traceback information not available)"
    else:
        # Get the file name where the exception occurred
        file_name = exc_tb.tb_frame.f_code.co_filename

        # Create a formatted error message string with file name, line number, and the actual error
        line_number = exc_tb.tb_lineno
        error_message = f"Error occurred in python script: [{file_name}] at line number [{line_number}]: {str(error)}"

    # Log the error for better tracking
    logging.error(error_message)

    return error_message


class CustomException(Exception):
    """
    Custom exception class for handling errors in the US visa application.
    """

    def __init__(self, error: Exception, error_detail: types.ModuleType): # Use types.ModuleType
        """
        Initializes the USvisaException with a detailed error message.

        :param error: The exception object.
        :param error_detail: The sys module to access traceback details.
        """
        # Call the base class constructor with the string representation of the error
        super().__init__(str(error))

        # Format the detailed error message using the error_message_detail function
        self.error_message = error_message_detail(error, error_detail)

    def __str__(self) -> str:
        """
        Returns the string representation of the error message.
        """
        return self.error_message