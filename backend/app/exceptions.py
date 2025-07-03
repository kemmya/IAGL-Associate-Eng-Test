
"""
Custom exceptions for the TODO application.
Provides specific exception classes for different error scenarios.
"""

from typing import Optional

class TodoAppException(Exception):
    """Base exception class for all TODO application exceptions."""
    
    def __init__(self, message: str, error_code: str = "UNKNOWN ERROR"):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.error_code = error_code or "UNKNOWN ERROR"


class TodoNotFoundError(TodoAppException):
    """Exception raised when a todo item is not found."""
    
    def __init__(self, message: str = "Todo not found"):
        super().__init__(message, "TODO_NOT_FOUND")


class ValidationError(TodoAppException):
    """Exception raised when data validation fails."""
    
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, "VALIDATION_ERROR")


class StorageError(TodoAppException):
    """Exception raised when storage operations fail."""
    
    def __init__(self, message: str = "Storage operation failed"):
        super().__init__(message, "STORAGE_ERROR")