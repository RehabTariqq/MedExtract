class MedExtractException(Exception):
    """Base exception for all MedExtract-specific errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(MedExtractException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ValidationException(MedExtractException):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=422)