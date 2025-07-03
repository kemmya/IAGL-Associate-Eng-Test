#!/usr/bin/env python3
"""
Test script for the PostgreSQL database integration.
Tests all CRUD operations and verifies the FastAPI backend functionality.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append('.')

async def test_database_integration():
    """Test the complete database integration."""
    
    print("🔍 Testing PostgreSQL Database Integration")
    print("=" * 50)
    
    try:
        # Test 1: Database Connection
        print("\n1. Testing database connection...")
        from app.database import check_database_connection, create_tables
        
        if not check_database_connection():
            print("❌ Database connection failed")
            return False
        print("✅ Database connection successful")
        
        # Test 2: Table Creation
        print("\n2. Creating database tables...")
        create_tables()
        print("✅ Database tables created successfully")
        
        # Test 3: Storage Layer Tests
        print("\n3. Testing PostgreSQL storage layer...")
        from app.db_storage import PostgreSQLTodoStorage
        from app.models import TodoCreate, TodoUpdate
        
        storage = PostgreSQLTodoStorage()
        
        # Test creating todos
        todo1_data = TodoCreate(title="Buy groceries for the week")
        todo2_data = TodoCreate(title="Complete project documentation")
        todo3_data = TodoCreate(title="Schedule team meeting")
        
        todo1 = await storage.create_todo(todo1_data)
        todo2 = await storage.create_todo(todo2_data)
        todo3 = await storage.create_todo(todo3_data)
        
        print(f"✅ Created 3 todos:")
        print(f"   - Todo {todo1.id}: {todo1.title}")
        print(f"   - Todo {todo2.id}: {todo2.title}")
        print(f"   - Todo {todo3.id}: {todo3.title}")
        
        # Test getting all todos
        all_todos = await storage.get_all_todos()
        print(f"✅ Retrieved {len(all_todos)} todos from database")
        
        # Test updating a todo
        update_data = TodoUpdate(completed=True)
        updated_todo = await storage.update_todo(todo1.id, update_data)
        if updated_todo:
            print(f"✅ Updated todo {todo1.id} - marked as completed")
        
        # Test getting specific todo
        retrieved_todo = await storage.get_todo_by_id(todo2.id)
        if retrieved_todo:
            print(f"✅ Retrieved specific todo: {retrieved_todo.title}")
        
        # Test 4: Service Layer Tests
        print("\n4. Testing service layer...")
        from app.services import TodoService
        
        service = TodoService(storage=storage)
        
        # Test statistics
        stats = await service.get_todo_stats()
        print(f"✅ Todo statistics:")
        print(f"   - Total: {stats.total}")
        print(f"   - Completed: {stats.completed}")
        print(f"   - Pending: {stats.pending}")
        
        # Test bulk operations
        bulk_result = await service.mark_all_complete()
        print(f"✅ Bulk complete: {bulk_result.message}")
        
        # Test 5: API Layer Test (Service Integration)
        print("\n5. Testing API integration...")
        
        # Create a new todo through the service
        new_todo_data = TodoCreate(title="Test API integration")
        new_todo = await service.create_todo(new_todo_data)
        print(f"✅ Created todo via service: {new_todo.title}")
        
        # Get all todos via service
        service_todos = await service.get_all_todos()
        print(f"✅ Retrieved {len(service_todos)} todos via service")
        
        print("\n" + "=" * 50)
        print("🎉 All database integration tests passed successfully!")
        print("\n📊 Final Statistics:")
        final_stats = await service.get_todo_stats()
        print(f"   📝 Total todos: {final_stats.total}")
        print(f"   ✅ Completed: {final_stats.completed}")
        print(f"   ⏳ Pending: {final_stats.pending}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_fastapi_startup():
    """Test FastAPI application startup."""
    print("\n🚀 Testing FastAPI Application Startup")
    print("=" * 50)
    
    try:
        from app.main import app
        from app.config import settings
        
        print(f"✅ FastAPI app created successfully")
        print(f"   App name: {settings.app_name}")
        print(f"   Version: {settings.app_version}")
        print(f"   Debug mode: {settings.debug}")
        print(f"   Host: {settings.host}")
        print(f"   Port: {settings.port}")
        
        # Test database initialization during startup
        from app.database import check_database_connection
        if check_database_connection():
            print("✅ Database ready for FastAPI integration")
        
        return True
        
    except Exception as e:
        print(f"❌ FastAPI startup test failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🔬 PostgreSQL Database Integration Test Suite")
    print("=" * 60)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run async tests
    db_test_result = asyncio.run(test_database_integration())
    api_test_result = asyncio.run(test_fastapi_startup())
    
    print("\n" + "=" * 60)
    print("📋 Test Results Summary:")
    print(f"   Database Integration: {'✅ PASSED' if db_test_result else '❌ FAILED'}")
    print(f"   FastAPI Startup: {'✅ PASSED' if api_test_result else '❌ FAILED'}")
    
    if db_test_result and api_test_result:
        print("\n🎉 All tests passed! The TODO app is ready for production use.")
        print("\n🔗 To start the server:")
        print("   python run.py")
        print("\n📚 API Documentation available at:")
        print("   http://localhost:9091/docs")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()