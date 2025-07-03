
"""
Storage layer for the TODO application.
Provides in-memory storage with interfaces that can be easily extended to support databases.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime
import asyncio
from threading import Lock

from .models import Todo, TodoCreate, TodoUpdate


class TodoStorage(ABC):
    """Abstract base class for TODO storage implementations."""
    
    @abstractmethod
    async def get_all_todos(self) -> List[Todo]:
        """Retrieve all todos."""
        pass
    
    @abstractmethod
    async def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """Retrieve a todo by its ID."""
        pass
    
    @abstractmethod
    async def create_todo(self, todo_data: TodoCreate) -> Todo:
        """Create a new todo."""
        pass
    
    @abstractmethod
    async def update_todo(self, todo_id: int, update_data: TodoUpdate) -> Optional[Todo]:
        """Update an existing todo."""
        pass
    
    @abstractmethod
    async def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo by its ID."""
        pass
    
    @abstractmethod
    async def mark_all_complete(self) -> int:
        """Mark all todos as complete and return the count of affected items."""
        pass
    
    @abstractmethod
    async def delete_completed_todos(self) -> int:
        """Delete all completed todos and return the count of deleted items."""
        pass
    
    @abstractmethod
    async def delete_all_todos(self) -> int:
        """Delete all todos and return the count of deleted items."""
        pass


class InMemoryTodoStorage(TodoStorage):
    """In-memory implementation of TodoStorage for development and testing."""
    
    def __init__(self):
        self._todos: Dict[int, Todo] = {}
        self._next_id = 1
        self._lock = Lock()  # Thread-safe operations
    
    async def get_all_todos(self) -> List[Todo]:
        """Retrieve all todos sorted by creation date (newest first)."""
        with self._lock:
            todos = list(self._todos.values())
            return sorted(todos, key=lambda t: t.created_at, reverse=True)
    
    async def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """Retrieve a todo by its ID."""
        with self._lock:
            return self._todos.get(todo_id)
    
    async def create_todo(self, todo_data: TodoCreate) -> Todo:
        """Create a new todo."""
        with self._lock:
            todo_id = self._next_id
            self._next_id += 1
            
            todo = Todo(
                id=todo_id,
                title=todo_data.title,
                completed=False,
                created_at=datetime.utcnow()
            )
            
            self._todos[todo_id] = todo
            return todo
    
    async def update_todo(self, todo_id: int, update_data: TodoUpdate) -> Optional[Todo]:
        """Update an existing todo."""
        with self._lock:
            if todo_id not in self._todos:
                return None
            
            current_todo = self._todos[todo_id]
            
            # Create updated todo with new values
            update_dict = update_data.model_dump(exclude_unset=True)
            
            # Create new todo instance with updated fields
            updated_todo = Todo(
                id=current_todo.id,
                title=update_dict.get('title', current_todo.title),
                completed=update_dict.get('completed', current_todo.completed),
                created_at=current_todo.created_at
            )
            
            self._todos[todo_id] = updated_todo
            return updated_todo
    
    async def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo by its ID."""
        with self._lock:
            if todo_id in self._todos:
                del self._todos[todo_id]
                return True
            return False
    
    async def mark_all_complete(self) -> int:
        """Mark all todos as complete and return the count of affected items."""
        with self._lock:
            affected_count = 0
            for todo_id, todo in self._todos.items():
                if not todo.completed:
                    updated_todo = Todo(
                        id=todo.id,
                        title=todo.title,
                        completed=True,
                        created_at=todo.created_at
                    )
                    self._todos[todo_id] = updated_todo
                    affected_count += 1
            return affected_count
    
    async def delete_completed_todos(self) -> int:
        """Delete all completed todos and return the count of deleted items."""
        with self._lock:
            completed_ids = [
                todo_id for todo_id, todo in self._todos.items() 
                if todo.completed
            ]
            
            for todo_id in completed_ids:
                del self._todos[todo_id]
            
            return len(completed_ids)
    
    async def delete_all_todos(self) -> int:
        """Delete all todos and return the count of deleted items."""
        with self._lock:
            count = len(self._todos)
            self._todos.clear()
            return count


# Global storage instance - can be easily swapped for database implementation
todo_storage = InMemoryTodoStorage()