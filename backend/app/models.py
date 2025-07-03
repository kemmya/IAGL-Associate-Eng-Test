
"""
Data models for the TODO application.
Defines Pydantic models for request/response validation and SQLAlchemy models for database operations.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TodoBase(BaseModel):
    """Base model for TODO items with common fields."""
    title: str = Field(..., min_length=1, max_length=500, description="The todo task description")


class TodoCreate(TodoBase):
    """Model for creating a new TODO item."""
    pass


class TodoUpdate(BaseModel):
    """Model for updating a TODO item."""
    completed: Optional[bool] = Field(None, description="Whether the todo is completed")
    title: Optional[str] = Field(None, min_length=1, max_length=500, description="Updated task description")


class Todo(TodoBase):
    """Complete TODO model with all fields."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Unique identifier for the todo")
    completed: bool = Field(default=False, description="Whether the todo is completed")
    created_at: datetime = Field(..., description="When the todo was created")


class TodoStats(BaseModel):
    """Statistics about TODO items."""
    total: int = Field(..., description="Total number of todos")
    completed: int = Field(..., description="Number of completed todos")
    pending: int = Field(..., description="Number of pending todos")


class BulkActionResponse(BaseModel):
    """Response model for bulk operations."""
    message: str = Field(..., description="Description of the action performed")
    affected_count: int = Field(..., description="Number of items affected")


class ErrorResponse(BaseModel):
    """Standard error response model."""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Specific error code")