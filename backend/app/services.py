
"""
Business logic layer for the TODO application.
Contains service classes that handle complex business operations and validation.
"""

from typing import List, Optional
import logging
from datetime import datetime

from .models import Todo, TodoCreate, TodoUpdate, TodoStats, BulkActionResponse
from .storage import TodoStorage, todo_storage
from app.exceptions import TodoNotFoundError, ValidationError

logger = logging.getLogger(__name__)


class TodoService:
    """Service class for managing TODO operations with business logic."""
    
    def __init__(self, storage: Optional[TodoStorage] = None):
        self.storage = storage or todo_storage
    
    async def get_all_todos(self) -> List[Todo]:
        """Retrieve all todos."""
        try:
            todos = await self.storage.get_all_todos()
            logger.info(f"Retrieved {len(todos)} todos")
            return todos
        except Exception as e:
            logger.error(f"Error retrieving todos: {str(e)}")
            raise
    
    async def get_todo_by_id(self, todo_id: int) -> Todo:
        """Retrieve a todo by ID, raising exception if not found."""
        if todo_id <= 0:
            raise ValidationError("Todo ID must be a positive integer")
        
        todo = await self.storage.get_todo_by_id(todo_id)
        if not todo:
            raise TodoNotFoundError(f"Todo with ID {todo_id} not found")
        
        logger.info(f"Retrieved todo {todo_id}: {todo.title}")
        return todo
    
    async def create_todo(self, todo_data: TodoCreate) -> Todo:
        """Create a new todo with validation."""
        # Additional business validation
        if not todo_data.title.strip():
            raise ValidationError("Todo title cannot be empty or only whitespace")
        
        # Sanitize input
        sanitized_data = TodoCreate(title=todo_data.title.strip())
        
        try:
            todo = await self.storage.create_todo(sanitized_data)
            logger.info(f"Created new todo {todo.id}: {todo.title}")
            return todo
        except Exception as e:
            logger.error(f"Error creating todo: {str(e)}")
            raise
    
    async def update_todo(self, todo_id: int, update_data: TodoUpdate) -> Todo:
        """Update an existing todo."""
        if todo_id <= 0:
            raise ValidationError("Todo ID must be a positive integer")
        
        # Validate that we have something to update
        if not any(field is not None for field in [update_data.title, update_data.completed]):
            raise ValidationError("At least one field must be provided for update")
        
        # Sanitize title if provided
        if update_data.title is not None:
            if not update_data.title.strip():
                raise ValidationError("Todo title cannot be empty or only whitespace")
            update_data.title = update_data.title.strip()
        
        updated_todo = await self.storage.update_todo(todo_id, update_data)
        if not updated_todo:
            raise TodoNotFoundError(f"Todo with ID {todo_id} not found")
        
        logger.info(f"Updated todo {todo_id}: {updated_todo.title}")
        return updated_todo
    
    async def delete_todo(self, todo_id: int) -> None:
        """Delete a todo by ID."""
        if todo_id <= 0:
            raise ValidationError("Todo ID must be a positive integer")
        
        deleted = await self.storage.delete_todo(todo_id)
        if not deleted:
            raise TodoNotFoundError(f"Todo with ID {todo_id} not found")
        
        logger.info(f"Deleted todo {todo_id}")
    
    async def get_todo_stats(self) -> TodoStats:
        """Get statistics about todos."""
        todos = await self.storage.get_all_todos()
        
        total = len(todos)
        completed = sum(1 for todo in todos if todo.completed)
        pending = total - completed
        
        stats = TodoStats(total=total, completed=completed, pending=pending)
        logger.info(f"Generated stats: {stats}")
        return stats
    
    async def mark_all_complete(self) -> BulkActionResponse:
        """Mark all todos as complete."""
        try:
            affected_count = await self.storage.mark_all_complete()
            message = f"Marked {affected_count} todos as complete"
            logger.info(message)
            return BulkActionResponse(message=message, affected_count=affected_count)
        except Exception as e:
            logger.error(f"Error marking all todos complete: {str(e)}")
            raise
    
    async def delete_completed_todos(self) -> BulkActionResponse:
        """Delete all completed todos."""
        try:
            deleted_count = await self.storage.delete_completed_todos()
            message = f"Deleted {deleted_count} completed todos"
            logger.info(message)
            return BulkActionResponse(message=message, affected_count=deleted_count)
        except Exception as e:
            logger.error(f"Error deleting completed todos: {str(e)}")
            raise
    
    async def delete_all_todos(self) -> BulkActionResponse:
        """Delete all todos."""
        try:
            deleted_count = await self.storage.delete_all_todos()
            message = f"Deleted {deleted_count} todos"
            logger.info(message)
            return BulkActionResponse(message=message, affected_count=deleted_count)
        except Exception as e:
            logger.error(f"Error deleting all todos: {str(e)}")
            raise


# Global service instance
todo_service = TodoService()