
#!/usr/bin/env python3
"""
Demonstration script showing the Python FastAPI TODO application functionality.
This script tests all the core API endpoints without requiring a running server.
"""

import sys
import os
import asyncio
from typing import List

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import Todo, TodoCreate, TodoUpdate
from app.services import TodoService
from app.storage import InMemoryTodoStorage


async def demo_api_functionality():
    """Demonstrate all the API functionality."""
    print("🐍 Python FastAPI TODO Application Demo")
    print("=" * 50)
    
    # Initialize service with fresh storage
    storage = InMemoryTodoStorage()
    service = TodoService(storage)
    
    print("\n1. Creating sample todos...")
    todos_to_create = [
        TodoCreate(title="Learn Python FastAPI"),
        TodoCreate(title="Build production-ready API"),
        TodoCreate(title="Write comprehensive tests"),
        TodoCreate(title="Deploy to production")
    ]
    
    created_todos = []
    for todo_data in todos_to_create:
        todo = await service.create_todo(todo_data)
        created_todos.append(todo)
        print(f"   ✓ Created: {todo.title} (ID: {todo.id})")
    
    print(f"\n2. Retrieving all todos...")
    all_todos = await service.get_all_todos()
    print(f"   Total todos: {len(all_todos)}")
    for todo in all_todos:
        status = "✓" if todo.completed else "○"
        print(f"   {status} {todo.title}")
    
    print(f"\n3. Getting todo statistics...")
    stats = await service.get_todo_stats()
    print(f"   Total: {stats.total}, Completed: {stats.completed}, Pending: {stats.pending}")
    
    print(f"\n4. Updating a todo (marking as complete)...")
    first_todo_id = created_todos[0].id
    update_data = TodoUpdate(completed=True)
    updated_todo = await service.update_todo(first_todo_id, update_data)
    print(f"   ✓ Marked complete: {updated_todo.title}")
    
    print(f"\n5. Getting individual todo...")
    retrieved_todo = await service.get_todo_by_id(first_todo_id)
    status = "✓" if retrieved_todo.completed else "○"
    print(f"   {status} {retrieved_todo.title} (ID: {retrieved_todo.id})")
    
    print(f"\n6. Bulk operations...")
    
    # Mark all remaining as complete
    bulk_result = await service.mark_all_complete()
    print(f"   ✓ {bulk_result.message}")
    
    # Get updated stats
    updated_stats = await service.get_todo_stats()
    print(f"   Updated stats - Total: {updated_stats.total}, Completed: {updated_stats.completed}")
    
    print(f"\n7. Testing error handling...")
    try:
        await service.get_todo_by_id(999)
    except Exception as e:
        print(f"   ✓ Correctly handled error: {type(e).__name__}")
    
    try:
        await service.create_todo(TodoCreate(title=""))
    except Exception as e:
        print(f"   ✓ Correctly handled validation error: {type(e).__name__}")
    
    print(f"\n8. Cleanup - deleting all todos...")
    delete_result = await service.delete_all_todos()
    print(f"   ✓ {delete_result.message}")
    
    final_todos = await service.get_all_todos()
    print(f"   Final count: {len(final_todos)} todos")
    
    print(f"\n🎉 Demo completed successfully!")
    print("=" * 50)
    print("Features demonstrated:")
    print("✓ Type-safe models with Pydantic")
    print("✓ Async/await operations")
    print("✓ Business logic validation")
    print("✓ Error handling")
    print("✓ In-memory storage")
    print("✓ Service layer architecture")
    print("✓ Bulk operations")
    print("✓ CRUD operations")


def demo_models():
    """Demonstrate the Pydantic models."""
    print("\n📋 Pydantic Models Demo")
    print("-" * 30)
    
    # Test TodoCreate validation
    print("Creating TodoCreate model:")
    try:
        valid_create = TodoCreate(title="Valid todo")
        print(f"   ✓ Valid: {valid_create.title}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        invalid_create = TodoCreate(title="")
        print(f"   ✗ Should not reach here")
    except Exception as e:
        print(f"   ✓ Correctly rejected empty title: {type(e).__name__}")
    
    # Test TodoUpdate model
    print("\nCreating TodoUpdate model:")
    update = TodoUpdate(completed=True)
    print(f"   ✓ Update model: completed={update.completed}")
    
    # Test model serialization
    print("\nModel serialization:")
    print(f"   JSON: {valid_create.model_dump_json()}")


if __name__ == "__main__":
    print("🚀 Starting Python FastAPI TODO Application Demo\n")
    
    # Demo the models
    demo_models()
    
    # Demo the async API functionality
    asyncio.run(demo_api_functionality())
    
    print("\n💡 To run the full FastAPI server:")
    print("   python start_python_server.py")
    print("\n📚 API Documentation (when server is running):")
    print("   http://localhost:9091/docs")
    print("   http://localhost:9091/health")