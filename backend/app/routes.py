
"""
API routes for the TODO application.
Defines FastAPI endpoints with proper validation, error handling, and documentation.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
import logging

from .models import Todo, TodoCreate, TodoUpdate, TodoStats, BulkActionResponse, ErrorResponse
from .services import TodoService, todo_service
from .exceptions import TodoNotFoundError, ValidationError, TodoAppException

logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter(prefix="/api", tags=["todos"])


def get_todo_service() -> TodoService:
    """Dependency injection for TodoService."""
    return todo_service


@router.get(
    "/todos",
    response_model=List[Todo],
    summary="Get all todos",
    description="Retrieve all todo items sorted by creation date (newest first)."
)
async def get_todos(service: TodoService = Depends(get_todo_service)) -> List[Todo]:
    """Get all todos."""
    try:
        return await service.get_all_todos()
    except Exception as e:
        logger.error(f"Error in get_todos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve todos"
        )


@router.get(
    "/todos/{todo_id}",
    response_model=Todo,
    summary="Get todo by ID",
    description="Retrieve a specific todo by its ID.",
    responses={
        404: {"model": ErrorResponse, "description": "Todo not found"}
    }
)
async def get_todo(
    todo_id: int, 
    service: TodoService = Depends(get_todo_service)
) -> Todo:
    """Get a specific todo by ID."""
    try:
        return await service.get_todo_by_id(todo_id)
    except TodoNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in get_todo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve todo"
        )


@router.post(
    "/todos",
    response_model=Todo,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo",
    description="Create a new todo item with the provided data.",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input data"}
    }
)
async def create_todo(
    todo_data: TodoCreate,
    service: TodoService = Depends(get_todo_service)
) -> Todo:
    """Create a new todo."""
    try:
        return await service.create_todo(todo_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in create_todo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create todo"
        )


@router.put(
    "/todos/{todo_id}",
    response_model=Todo,
    summary="Update a todo",
    description="Update an existing todo item.",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        404: {"model": ErrorResponse, "description": "Todo not found"}
    }
)
async def update_todo(
    todo_id: int,
    update_data: TodoUpdate,
    service: TodoService = Depends(get_todo_service)
) -> Todo:
    """Update an existing todo."""
    try:
        return await service.update_todo(todo_id, update_data)
    except TodoNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in update_todo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update todo"
        )


@router.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo",
    description="Delete a specific todo by its ID.",
    responses={
        404: {"model": ErrorResponse, "description": "Todo not found"}
    }
)
async def delete_todo(
    todo_id: int,
    service: TodoService = Depends(get_todo_service)
) -> None:
    """Delete a todo."""
    try:
        await service.delete_todo(todo_id)
    except TodoNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in delete_todo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete todo"
        )


@router.get(
    "/todos/stats",
    response_model=TodoStats,
    summary="Get todo statistics",
    description="Get statistics about todos (total, completed, pending)."
)
async def get_todo_stats(
    service: TodoService = Depends(get_todo_service)
) -> TodoStats:
    """Get todo statistics."""
    try:
        return await service.get_todo_stats()
    except Exception as e:
        logger.error(f"Error in get_todo_stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve todo statistics"
        )


# Bulk operations
@router.post(
    "/todos/bulk/mark-complete",
    response_model=BulkActionResponse,
    summary="Mark all todos as complete",
    description="Mark all existing todos as complete."
)
async def mark_all_complete(
    service: TodoService = Depends(get_todo_service)
) -> BulkActionResponse:
    """Mark all todos as complete."""
    try:
        return await service.mark_all_complete()
    except Exception as e:
        logger.error(f"Error in mark_all_complete: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark todos as complete"
        )


@router.delete(
    "/todos/bulk/completed",
    response_model=BulkActionResponse,
    summary="Delete completed todos",
    description="Delete all completed todos."
)
async def delete_completed_todos(
    service: TodoService = Depends(get_todo_service)
) -> BulkActionResponse:
    """Delete all completed todos."""
    try:
        return await service.delete_completed_todos()
    except Exception as e:
        logger.error(f"Error in delete_completed_todos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete completed todos"
        )


@router.delete(
    "/todos/bulk/all",
    response_model=BulkActionResponse,
    summary="Delete all todos",
    description="Delete all todos. This action cannot be undone."
)
async def delete_all_todos(
    service: TodoService = Depends(get_todo_service)
) -> BulkActionResponse:
    """Delete all todos."""
    try:
        return await service.delete_all_todos()
    except Exception as e:
        logger.error(f"Error in delete_all_todos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete all todos"
        )