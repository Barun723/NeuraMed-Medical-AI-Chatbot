import sys

class CustomException(Exception):
    def __init__(self, message: str,get_detailed:Exception=None):
        self.error_message = self.get_detailed_error_message(message, get_detailed)
        super().__init__(self.error_message)
    @staticmethod
    def get_detailed_error_message(message, get_detailed):
        _, _, exc_tb = sys.exc_info()
        if exc_tb:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
        else:
            try:
                frame = sys._getframe(2)
                file_name = frame.f_code.co_filename
                line_number = frame.f_lineno
            except Exception:
                file_name = "Unknown"
                line_number = "Unknown"
        return f"{message} | Error: {get_detailed} | File: {file_name} | Line: {line_number}"
    def __str__(self):
        return self.error_message